import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image


load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

for frame_num in [58, 59, 60, 61]:
    img = Image.open(f"game_data/frame_{frame_num:04d}.png")
    
    prompt = f"""Frame {frame_num} - Analyze critically:
    
1. Where is dino? (ground/in air)
2. How many obstacles visible?
3. Distance of CLOSEST obstacle?
4. Any obstacles in sequence (multiple cacti close together)?"""
    
    result = model.generate_content([prompt, img])
    print(f"\n{'='*60}")
    print(f"FRAME {frame_num}")
    print(f"{'='*60}")

    print(result.text)

