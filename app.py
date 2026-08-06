import streamlit as st
import requests
import os

st.set_page_config(page_title="AI Video Studio", layout="centered")

st.title("🎬 AI Video Generation Studio")
st.write("Powered by FastAPI & ComfyUI")

# User Inputs
prompt_input = st.text_area(
    "Enter your video prompt:", 
    "An ancient warrior walking through a ruined temple surrounded by glowing blue flames, dramatic clouds, god rays, Unreal Engine 5"
)

negative_prompt_input = st.text_input(
    "Enter your negative prompt (what to avoid):", 
    "text, watermark, blurry, low quality, distorted"
)

if st.button("Generate Video 🚀"):
    with st.spinner("FastAPI server is requesting generation from ComfyUI... Please wait."):
        try:
            # Call FastAPI backend endpoint with both prompts
            api_endpoint = "http://127.0.0.1:8000/generate-video"
            response = requests.post(
                api_endpoint, 
                params={
                    "prompt_text": prompt_input,
                    "negative_prompt": negative_prompt_input
                }
            )

            if response.status_code == 200:
                data = response.json()
                video_path = data.get("local_path")

                st.success("Video generated and delivered successfully!")
                
                if video_path and os.path.exists(video_path):
                    st.video(video_path)
            else:
                st.error(f"Backend Error [{response.status_code}]: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI server. Make sure `server.py` is running on port 8000!")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")