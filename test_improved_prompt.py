import google.generativeai as genai
from PIL import Image

# Configure Gemini (REPLACE WITH YOUR API KEY)
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini with env variable
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def analyze_with_context(image_path, frame_number, score):
    """Analyze frame with improved context"""
    
    img = Image.open(image_path)
    
    prompt = f"""You are analyzing Frame {frame_number} from Chrome Dino game.

CRITICAL CONTEXT:
- Current score is {score}
- If score > 0, the game IS ACTIVELY RUNNING
- Ignore any "Press space to play" text if score > 0 - this is a UI bug
- The game IS running right now

YOUR TASK:
1. Locate the dino (small T-Rex on left side)
2. Identify ALL obstacles visible (black cacti or grey birds)
3. For EACH obstacle, estimate distance from dino in pixels
4. Determine if dino is on ground, jumping, or ducking

DECISION:
Based on obstacle distances, should the player:
- JUMP NOW (obstacle within 300-400px)
- WAIT (obstacle >400px away)
- DUCK (bird approaching)

Be specific with pixel distances.
"""
    
    response = model.generate_content([prompt, img])
    return response.text

# Test on frame 50
print("=" * 60)
print("ANALYZING FRAME 50 (Score: 75)")
print("=" * 60)

result = analyze_with_context("game_data/frame_0050.png", frame_number=50, score=75)
print(result)
print("\n")

print("=" * 60)
print("WHAT YOU ACTUALLY DID:")
print("=" * 60)
print("Frame 50: You pressed SPACE (jumped)")