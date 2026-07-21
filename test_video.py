import json
import urllib.request
import urllib.error
import random  # <-- 1. Add the random library

# 2. Load your SVD video blueprint
with open("svd_workflow_api.json", "r", encoding="utf-8") as file:
    video_workflow = json.load(file)

# 3. Force a fresh generation by randomizing the seed!
# REPLACE "3" WITH YOUR ACTUAL KSAMPLER NODE ID
sampler_id = "3" 
if sampler_id in video_workflow:
    # Generate a random 15-digit number
    new_seed = random.randint(100000000000000, 999999999999999) 
    video_workflow[sampler_id]["inputs"]["seed"] = new_seed

# 4. Wrap it in the payload format
payload = {"prompt": video_workflow}
data = json.dumps(payload).encode('utf-8')

# 5. Send the command to your local ComfyUI server
print("Sending video request to ComfyUI...")
req = urllib.request.Request(
    "http://127.0.0.1:8188/prompt", 
    data=data, 
    headers={'Content-Type': 'application/json'}
)

try:
    response = urllib.request.urlopen(req)
    print("Success! Video generation started. Receipt:", response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("\n--- ComfyUI Detailed Error Response ---")
    print(e.read().decode('utf-8'))
except Exception as e:
    print("Error triggering video:", e)