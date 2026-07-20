# AI-Game-Server & The Simulation Pipeline

A high-performance backend architecture designed to bridge game engines (such as Unreal Engine) with local Generative AI tools (ComfyUI) using a Python FastAPI server. This project enables real-time, dynamic asset and cutscene generation via programmatic API manipulation and asynchronous polling.

---

## 🛠️ Technical Architecture

1. **FastAPI Web Server (`main.py`):** Acts as the primary middleware listening for incoming HTTP requests from game clients.
2. **Dynamic Blueprint Modification:** Programmatically loads ComfyUI API node graphs (`workflow_api.json`), injects player prompts into text-encode nodes, and handles runtime model checkpoint swapping.
3. **Asynchronous Polling:** Submits jobs to ComfyUI's background engine, captures receipt IDs (`prompt_id`), and polls the `/history` endpoint until rendering completes without freezing the server.
4. **Binary Stream Retrieval:** Automatically fetches generated binary data from ComfyUI and streams it back to the client using FastAPI's `FileResponse`.

---

## 🎮 Game Concept: The Simulation

This backend serves as the technical engine for ***The Simulation***, an immersive narrative game featuring deep character progression and regional world-building.

### Premise
A seventeen-year-old boy avoids a fateful crossroad on his way home, but his father takes that same path and vanishes[cite: 1]. The father wakes inside a featureless, shrinking room, punches his way out into a jungle, and discovers the horrifying truth: his entire family has been plugged into a vast virtual-reality simulation[cite: 1]. The story follows each family member as they wake up separately and fight to survive and reunite[cite: 1].

### Character Journeys
* **The Grandmother:** Meets the simulation's initial traps with fury rather than panic, using brute force to smash through walls and charging headfirst into combat[cite: 1].
* **The Mother:** Driven by overprotection, she moves cautiously, avoids unnecessary conflict, and prioritizes finding her family over leveling up[cite: 1].
* **The Son:** Navigates jungle tutorials, wields a great sword, unlocks a berserk mode, and recruits an 8-year survivor named Prakash as an ally[cite: 1].
* **The Daughter:** Navigates sensory distress caused by her autism, tames a flying companion named Newton, and works to clear a "player killer" status to unlock family-contact features[cite: 1].

### The World
The map is divided into five regions named after members of Shiv ji's family (*Shiv ji, Maa Parvati ji, Ganesh ji, Kartikeya ji, and Ashok Sundari*), each featuring unique temples, guardian animals, and Asura adversaries[cite: 1].

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* ComfyUI installed locally with the `v1-5-pruned-emaonly.safetensors` model checkpoint.

### Installation & Execution
1. Clone the repository and navigate into the root folder.
2. Create and activate your virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
