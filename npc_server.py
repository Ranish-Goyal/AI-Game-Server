import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from openai import OpenAI
from sqlalchemy.orm import Session
from database import engine, Base, get_db, ChatMessage, User
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
import json

Base.metadata.create_all(bind=engine)
app = FastAPI(title="NPC Brain Engine API")

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1" 
)

# --- 1. AUTHENTICATION SETUP ---
SECRET_KEY = "my-super-secret-game-key" # In a real job, this goes in an .env file
ALGORITHM = "HS256"

# Sets up Bcrypt for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Tells FastAPI where the login route is
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") 

def get_password_hash(password):
    return pwd_context.hash(password)

# This dependency acts as our "Bouncer". It checks the JWT token on protected routes.
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
        
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# --- 2. DATA MODELS ---
class PlayerInput(BaseModel):
    text: str

class UserCreate(BaseModel):
    username: str
    password: str

# --- 3. PUBLIC ROUTES (No Token Needed) ---

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": f"User {user.username} created successfully!"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    # Generate the JWT Token good for 1 hour
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    encoded_jwt = jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": encoded_jwt, "token_type": "bearer"}

# --- 4. PROTECTED ROUTES (Requires JWT Token) ---

npc_database = {
    "Thorne": 'You are Thorne, gruff guardian of Eldrador. Reply strictly in JSON: {"dialogue": "words", "action": "idle | attack | point_way", "emotion": "calm | angry | protective"}.'
}

# Notice the new current_user dependency! You cannot run this without being logged in.
@app.post("/chat/{npc_name}")
def chat_with_npc(
    npc_name: str, 
    player_input: PlayerInput, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user) # <--- The Bouncer!
):
    # Fetch messages belonging ONLY to this specific user
    past_messages = db.query(ChatMessage).filter(
        ChatMessage.npc_name == npc_name,
        ChatMessage.user_id == current_user.id
    ).all()
    
    conversation_history = []
    
    if not past_messages:
        system_instruction = npc_database.get(npc_name, f'You are {npc_name}. Reply strictly in JSON: {{"dialogue": "words", "action": "idle", "emotion": "neutral"}}.')
        conversation_history.append({"role": "system", "content": system_instruction})
        db.add(ChatMessage(user_id=current_user.id, npc_name=npc_name, role="system", content=system_instruction))
    else:
        for msg in past_messages:
            conversation_history.append({"role": msg.role, "content": msg.content})

    conversation_history.append({"role": "user", "content": player_input.text})
    db.add(ChatMessage(user_id=current_user.id, npc_name=npc_name, role="user", content=player_input.text))
    db.commit()

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=conversation_history[-11:], 
            max_tokens=150,
            temperature=0.7,
            response_format={"type": "json_object"} 
        )
        
        npc_data = json.loads(response.choices[0].message.content)
        
        db.add(ChatMessage(user_id=current_user.id, npc_name=npc_name, role="assistant", content=json.dumps(npc_data)))
        db.commit()
        
        return {
            "npc_name": npc_name,
            "player": current_user.username,
            "dialogue": npc_data.get("dialogue", "Error"),
            "action": npc_data.get("action", "idle"),
            "emotion": npc_data.get("emotion", "neutral")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))