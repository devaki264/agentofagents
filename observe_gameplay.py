import time
import mss
import mss.tools
from pynput import keyboard
from datetime import datetime
import json
import os

# Setup
output_dir = "game_data"
os.makedirs(output_dir, exist_ok=True)

# Data storage
actions = []
frame_count = 0
recording = False

def on_press(key):
    """Log when human presses a key"""
    if not recording:
        return
    
    timestamp = time.time()
    try:
        key_name = key.char
    except AttributeError:
        key_name = str(key)
    
    action = {
        "timestamp": timestamp,
        "frame": frame_count,
        "action": key_name,
        "type": "keypress"
    }
    actions.append(action)
    print(f"[{timestamp:.2f}] Pressed: {key_name}")

# Start keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

print("=== Chrome Dino Game Observer ===")
print("Instructions:")
print("1. Position Chrome Dino game window on RIGHT side of screen")
print("2. Press ENTER to start recording")
print("3. Play the game normally (use SPACE to jump)")
print("4. Press Ctrl+C when done")
input("\nPress ENTER when ready...")

recording = True
start_time = time.time()

print("\n🔴 RECORDING - Play the game!")

try:
    with mss.mss() as sct:
        # Capture entire screen first (we'll adjust region later)
        monitor = sct.monitors[1]  # Primary monitor
        
        while True:
            # Capture frame
            frame_count += 1
            timestamp = time.time() - start_time
            
            screenshot = sct.grab(monitor)
            filename = f"{output_dir}/frame_{frame_count:04d}.png"
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=filename)
            
            # Log frame
            print(f"Frame {frame_count} captured at {timestamp:.2f}s", end='\r')
            
            time.sleep(0.1)  # Capture ~10 FPS
            
except KeyboardInterrupt:
    print("\n\n⏹️  Recording stopped!")
    
    # Save action log
    log_file = f"{output_dir}/actions.json"
    with open(log_file, 'w') as f:
        json.dump({
            "duration": time.time() - start_time,
            "frames": frame_count,
            "actions": actions
        }, f, indent=2)
    
    print(f"\n✅ Saved {frame_count} frames")
    print(f"✅ Saved {len(actions)} actions to {log_file}")
    print(f"📁 Check {output_dir}/ folder")

listener.stop()