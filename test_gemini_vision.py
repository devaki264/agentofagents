import google.generativeai as genai
from PIL import Image
import json

# Configure Gemini
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini with env variable
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def analyze_frame(image_path, frame_number, action_data):
    """Analyze a game frame with Gemini Vision"""
    
    # Load image
    img = Image.open(image_path)
    
    # Check if there was an action at this frame
    action_at_frame = None
    for action in action_data['actions']:
        if action['frame'] == frame_number:
            action_at_frame = action['action']
            break
    
    # Create prompt
    prompt = f"""Analyze this Chrome Dino game screenshot (Frame {frame_number}).

IDENTIFY:
1. Dino state: Is it on the ground, jumping, or ducking?
2. Obstacles: List ALL cacti or birds visible. For each, estimate distance from dino in pixels.
3. Current score: What's the score shown?
4. Immediate danger: Is there an obstacle that requires action RIGHT NOW?

DECISION:
Based on this frame, what should the player do?
- JUMP (if obstacle approaching within ~300-400px)
- DUCK (if bird approaching)
- NOTHING (if safe)

"""
    
    if action_at_frame:
        prompt += f"\nNOTE: Human pressed {action_at_frame} at this exact frame."
    
    # Get response
    response = model.generate_content([prompt, img])
    
    return response.text

# Load actions data
with open('game_data/actions.json', 'r') as f:
    actions_data = json.load(f)

# Analyze key frames
key_frames = [38, 42, 50, 55, 59, 61, 75]

print("=== GEMINI VISION ANALYSIS ===\n")

for frame_num in key_frames:
    print(f"{'='*60}")
    print(f"FRAME {frame_num}")
    print(f"{'='*60}")
    
    try:
        result = analyze_frame(f"game_data/frame_{frame_num:04d}.png", frame_num, actions_data)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n")