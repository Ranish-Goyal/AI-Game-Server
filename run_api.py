import json
import requests
import time

with open("workflow_api.json", "r", encoding="utf-8") as file:
    blueprint = json.load(file)

blueprint["7"]["inputs"]["text"] = "glitchy, lagging, corrupted game file"
blueprint["4"]["inputs"]["ckpt_name"] = "v1-5-pruned-emaonly.safetensors"

payload = {"prompt": blueprint}
url = "http://127.0.0.1:8188/prompt"

print("Sending request to ComfyUI...")
response = requests.post(url, json=payload).json()
prompt_id = response["prompt_id"]
print(f"Job accepted! Receipt ID: {prompt_id}")

print("Waiting for generation to finish...")
while True:
    history_url = f"http://127.0.0.1:8188/history/{prompt_id}"
    history_response = requests.get(history_url).json()
    
    if prompt_id in history_response:
        print("\nSUCCESS! The image is done rendering.")
        
        # --- NEW: STEP 5.5 (RETRIEVING THE FILE) ---
        # 1. Dig into the history dictionary to find the outputs
        outputs = history_response[prompt_id]["outputs"]
        
        # 2. Look through the outputs to find the node that saved the image (usually Node 9)
        for node_id in outputs:
            if "images" in outputs[node_id]:
                # Grab the exact filename ComfyUI generated
                image_filename = outputs[node_id]["images"][0]["filename"]
                print(f"Found image name: {image_filename}")
                
                # 3. Download the actual image bytes from ComfyUI's /view endpoint
                image_url = f"http://127.0.0.1:8188/view?filename={image_filename}"
                image_data = requests.get(image_url).content
                
                # 4. Save a copy of it right next to our Python script!
                with open("final_game_asset.png", "wb") as f:
                    f.write(image_data)
                    
                print("Image successfully downloaded to your Python folder!")
                break # Exit the loop since we found our image
                
        break # Exit the while loop
    
    print(".", end="", flush=True)
    time.sleep(2)