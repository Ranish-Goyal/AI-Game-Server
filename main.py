import json
import requests
import time
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

# 1. Define what data Unreal Engine is allowed to send us
class GameRequest(BaseModel):
    player_prompt: str

# 2. Create the web endpoint for Unreal Engine to hit
@app.post("/generate_cutscene")
def generate_cutscene(request: GameRequest):
    print(f"Unreal Engine requested: {request.player_prompt}")
    
    # 3. Load the blueprint
    with open("workflow_api.json", "r", encoding="utf-8") as file:
        blueprint = json.load(file)

    # 4. Inject the dynamically generated prompt from Unreal Engine!
    # (Assuming Node 6 is your Positive Prompt based on standard templates)
    blueprint["6"]["inputs"]["text"] = request.player_prompt 
    
    # Ensure the optimized model is used
    blueprint["4"]["inputs"]["ckpt_name"] = "v1-5-pruned-emaonly.safetensors"

    # 5. Send to ComfyUI
    payload = {"prompt": blueprint}
    url = "http://127.0.0.1:8188/prompt"
    response = requests.post(url, json=payload).json()
    prompt_id = response["prompt_id"]
    
    # 6. Wait for the render (Polling)
    while True:
        history_response = requests.get(f"http://127.0.0.1:8188/history/{prompt_id}").json()
        
        if prompt_id in history_response:
            outputs = history_response[prompt_id]["outputs"]
            for node_id in outputs:
                if "images" in outputs[node_id]:
                    image_filename = outputs[node_id]["images"][0]["filename"]
                    
                    # 7. Download the final image
                    image_url = f"http://127.0.0.1:8188/view?filename={image_filename}"
                    image_data = requests.get(image_url).content
                    
                    # Save it locally
                    with open("final_game_asset.png", "wb") as f:
                        f.write(image_data)
                        
                    # 8. Send the image file straight back to Unreal Engine!
                    return FileResponse("final_game_asset.png", media_type="image/png")
        
        time.sleep(2)