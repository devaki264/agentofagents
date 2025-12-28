import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import json

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel('gemini-2.0-flash-exp')

def analyze_frame(image_path, frame_number):
    """Quick analysis: obstacle distance only"""
    img = Image.open(image_path)
    
    prompt = f"""Frame {frame_number} - Chrome Dino game is RUNNING.

Quick analysis:
1. Is there an obstacle within 400px of the dino?
2. If yes, how far (estimate in pixels)?
3. Should player jump based on distance?

Be brief and specific."""
    
    response = model.generate_content([prompt, img])
    return response.text

# Load your jump data
with open('game_data/actions.json', 'r') as f:
    data = json.load(f)

# Get frames where you jumped (exclude frame 10 and 75)
jump_frames = [38, 42, 50, 55, 59, 61]

print("=" * 70)
print("TESTING RULE: 'Jump when obstacle within 350-400px'")
print("=" * 70)
print()

for frame_num in jump_frames:
    print(f"--- FRAME {frame_num} ---")
    print(f"What you did: Pressed SPACE (jumped)")
    print()
    
    result = analyze_frame(f"game_data/frame_{frame_num:04d}.png", frame_num)
    print("Gemini analysis:")
    print(result)
    print()
    print("-" * 70)
    print()

# ============== ADD THIS NEW CODE BELOW ============== 

print("\n" + "=" * 70)
print("RE-ANALYZING FRAME 50 WITH DETAILED PROMPT")
print("=" * 70)

img = Image.open("game_data/frame_0050.png")
detailed_prompt = """Frame 50 - Chrome Dino game is RUNNING (score 75).

DETAILED ANALYSIS:
1. Locate the dino precisely
2. Scan entire screen for ALL obstacles (cacti and birds)
3. For EACH obstacle found, estimate distance in pixels
4. List them all

Be thorough - check carefully for obstacles at ANY distance."""

response = model.generate_content([detailed_prompt, img])
print(response.text)