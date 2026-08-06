import json
import urllib.request
import urllib.parse
import random
import time
import os
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="AI Game Server API", version="1.0")

COMFYUI_URL = "http://127.0.0.1:8188"

@app.get("/")
def read_root():
    return {"status": "online", "message": "AI Game Server API is running."}

@app.post("/generate-video")
def generate_video(
    prompt_text: str = Query(..., description="Text prompt for video generation"),
    negative_prompt: str = Query("text, watermark", description="Negative prompt for video generation")
):
    # 1. Load SVD workflow
    if not os.path.exists("svd_workflow_api.json"):
        raise HTTPException(status_code=404, detail="svd_workflow_api.json file not found.")

    with open("svd_workflow_api.json", "r", encoding="utf-8") as f:
        workflow = json.load(f)

    # 2. Randomize seed and inject positive & negative prompts
    sampler_id = "3"
    prompt_node_id = "18"      # Positive prompt node
    negative_node_id = "19"    # Negative prompt node

    if sampler_id in workflow:
        workflow[sampler_id]["inputs"]["seed"] = random.randint(100000000000000, 999999999999999)
    
    if prompt_node_id in workflow:
        workflow[prompt_node_id]["inputs"]["text"] = prompt_text
    else:
        raise HTTPException(status_code=400, detail=f"Node {prompt_node_id} not found in workflow JSON.")

    if negative_node_id in workflow:
        workflow[negative_node_id]["inputs"]["text"] = negative_prompt
    else:
        raise HTTPException(status_code=400, detail=f"Node {negative_node_id} not found in workflow JSON.")

    # 3. Trigger ComfyUI API
    payload = json.dumps({"prompt": workflow}).encode("utf-8")
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt", 
        data=payload, 
        headers={"Content-Type": "application/json"}
    )

    try:
        response = urllib.request.urlopen(req)
        res_data = json.loads(response.read().decode("utf-8"))
        prompt_id = res_data["prompt_id"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to ComfyUI: {e}")

    # 4. Poll ComfyUI /history endpoint for completion
    filename = None
    subfolder = ""
    folder_type = "output"

    for _ in range(300):
        time.sleep(2)
        try:
            hist_req = urllib.request.urlopen(f"{COMFYUI_URL}/history/{prompt_id}")
            history = json.loads(hist_req.read().decode("utf-8"))
            
            if prompt_id in history:
                outputs = history[prompt_id].get("outputs", {})
                for node_id, node_output in outputs.items():
                    media_list = (
                        node_output.get("gifs") or 
                        node_output.get("images") or 
                        node_output.get("videos")
                    )
                    if media_list:
                        filename = media_list[0]["filename"]
                        subfolder = media_list[0].get("subfolder", "")
                        folder_type = media_list[0].get("type", "output")
                        break
                if filename:
                    break
        except Exception:
            pass

    if not filename:
        raise HTTPException(status_code=504, detail="Video rendering timed out.")

    # 5. Retrieve output file from ComfyUI /view endpoint
    query_params = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": folder_type})
    file_url = f"{COMFYUI_URL}/view?{query_params}"
    
    try:
        video_bytes = urllib.request.urlopen(file_url).read()
        output_filename = "latest_output.mp4"
        with open(output_filename, "wb") as f:
            f.write(video_bytes)
            
        return {
            "status": "success",
            "prompt_id": prompt_id,
            "filename": filename,
            "local_path": output_filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch rendered video file: {e}")