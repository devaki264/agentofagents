import os
import time
import mss
import mss.tools
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from pynput.keyboard import Key, Controller

# Load environment
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

keyboard = Controller()

def capture_game():
    """Capture current game screen"""
    with mss.mss() as sct:
        # Capture entire screen (we'll optimize later)
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        
        # Save temporarily
        mss.tools.to_png(screenshot.rgb, screenshot.size, output="temp_frame.png")
        return "temp_frame.png"

def analyze_frame(image_path):
    """Ask Gemini: should we jump?"""
    img = Image.open(image_path)
    
    prompt = """Chrome Dino game - QUICK DECISION NEEDED.

Answer in ONE sentence:
- Is there an obstacle within 300 pixels? 
- If YES: say "JUMP" and distance
- If NO: say "SAFE"

Be brief."""
    
    response = model.generate_content([prompt, img])
    return response.text

def should_jump(analysis):
    """Parse Gemini's response"""
    analysis_lower = analysis.lower()
    return "jump" in analysis_lower

def jump():
    """Press space to jump"""
    keyboard.press(Key.space)
    keyboard.release(Key.space)
    print("   🦘 JUMPED!")

def play_game():
    """Main game loop"""
    print("=" * 60)
    print("CHROME DINO AGENT - RULE #1")
    print("Rule: Jump when obstacle within 300px")
    print("=" * 60)
    print("\nStarting in 5 seconds...")
    print("1. Open Chrome Dino game")
    print("2. Click on game window")
    print("3. Wait for agent to start...")
    
    time.sleep(5)
    
    print("\n🎮 AGENT IS PLAYING!\n")
    
    frame_count = 0
    
    try:
        while True:
            frame_count += 1
            
            # Capture screen
            image_path = capture_game()
            
            # Analyze
            print(f"Frame {frame_count}: Analyzing...", end=" ")
            analysis = analyze_frame(image_path)
            
            # Decide
            if should_jump(analysis):
                print(f"Decision: JUMP | Reasoning: {analysis}")
                jump()
            else:
                print(f"Decision: SAFE | {analysis}")
            
            # Wait before next frame (don't spam API)
            time.sleep(0.5)  # Check every 0.5 seconds
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Agent stopped!")
        print(f"Total frames analyzed: {frame_count}")

if __name__ == "__main__":
    play_game()