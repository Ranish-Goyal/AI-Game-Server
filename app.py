import json
import urllib.request
import urllib.error
import random
import streamlit as st

st.set_page_config(page_title="AI Video Studio", layout="centered")

st.title("🎬 AI Video Generation Studio")
st.write("Generate high-quality AI video cutscenes using ComfyUI & Stable Video Diffusion!")

# Input prompt from user
prompt_input = st.text_area(
    "Enter your video prompt:", 
    "An ancient warrior walking through a ruined temple surrounded by glowing blue flames, dramatic clouds, god rays, Unreal Engine 5"
)

if st.button("Generate Video 🚀"):
    st.info("Sending request to ComfyUI server...")
    
    try:
        # 1. Load SVD workflow
        with open("svd_workflow_api.json", "r", encoding="utf-8") as f:
            workflow = json.load(f)
            
        # 2. Randomize seed to bypass cache
        sampler_id = "3"  # Adjust if your KSampler ID is different
        if sampler_id in workflow:
            workflow[sampler_id]["inputs"]["seed"] = random.randint(100000000000000, 999999999999999)
            
        # 3. Inject user prompt into text encode node (Node ID 6)
        if "18" in workflow:
            workflow["18"]["inputs"]["text"] = prompt_input

        # 4. Send request to local ComfyUI API
        payload = {"prompt": workflow}
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            "http://127.0.0.1:8188/prompt", 
            data=data, 
            headers={'Content-Type': 'application/json'}
        )
        
        response = urllib.request.urlopen(req)
        st.success("Generation started successfully! Check your ComfyUI window for rendering progress.")
        
    except Exception as e:
        st.error(f"Error triggering video generation: {e}")