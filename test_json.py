import json

# 1. Open the file and load the JSON blueprint into Python
with open("workflow_api.json", "r", encoding="utf-8") as file:
    blueprint = json.load(file)

# 2. Prove we can read the default text
print("--- OLD NEGATIVE PROMPT ---")
print(blueprint["7"]["inputs"]["text"])

# 3. Dynamically change the text!
blueprint["7"]["inputs"]["text"] = "glitchy, lagging, corrupted game file"

# 4. Prove that it changed
print("\n--- NEW NEGATIVE PROMPT ---")
print(blueprint["7"]["inputs"]["text"])