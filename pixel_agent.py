import cv2
import numpy as np
import mss
import time
from pynput.keyboard import Key, Controller

keyboard = Controller()

# Game configuration
DINO_X = 80
SCAN_Y_START = 200
SCAN_Y_END = 350
JUMP_THRESHOLD = 300

# Auto-stop configuration
MAX_FRAMES = 200  # Stop after this many frames (about 20 seconds at 0.1s delay)

def capture_game_region():
    """Capture just the game area"""
    with mss.mss() as sct:
        monitor = {
            "top": 150,
            "left": 400,
            "width": 800,
            "height": 400
        }
        
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        
        return img

def detect_obstacles_debug(img):
    """Find obstacles AND show what we're detecting"""
    
    # Threshold: dark pixels
    _, binary = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY_INV)
    
    # Create visualization
    debug_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    
    # Draw dino position
    cv2.line(debug_img, (DINO_X, 0), (DINO_X, img.shape[0]), (0, 255, 0), 2)
    
    # Draw scan region
    cv2.rectangle(debug_img, 
                  (0, SCAN_Y_START), 
                  (img.shape[1], SCAN_Y_END), 
                  (255, 0, 0), 2)
    
    obstacles = []
    
    for y in range(SCAN_Y_START, SCAN_Y_END):
        row = binary[y, :]
        
        # Find black pixels to the RIGHT of dino (ignore dino itself)
        black_pixels = np.where(row == 255)[0]
        black_pixels = black_pixels[black_pixels > DINO_X + 50]  # Ignore 50px around dino
        
        if len(black_pixels) > 0:
            obstacle_x = black_pixels[0]
            obstacles.append(obstacle_x)
            
            # Draw detection point
            cv2.circle(debug_img, (int(obstacle_x), y), 2, (0, 0, 255), -1)
    
    if obstacles:
        closest = min(obstacles)
        
        # Draw line to closest obstacle
        cv2.line(debug_img, (DINO_X, SCAN_Y_START), (int(closest), SCAN_Y_START), (255, 255, 0), 2)
        
        # Show distance
        distance = closest - DINO_X
        cv2.putText(debug_img, f"Distance: {distance}px", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Show debug window
        cv2.imshow('Agent Vision', debug_img)
        cv2.waitKey(1)
        
        return distance
    
    # Show debug window
    cv2.imshow('Agent Vision', debug_img)
    cv2.waitKey(1)
    
    return None

def play_game_debug():
    """Debug mode - shows what agent sees"""
    print("=" * 70)
    print("PIXEL AGENT - DEBUG MODE")
    print("=" * 70)
    print("\nYou'll see a window showing what the agent detects")
    print("Green line = Dino position")
    print("Blue box = Scan region")
    print("Red dots = Detected obstacles")
    print("Yellow line = Distance to closest obstacle")
    print(f"\nWill run for {MAX_FRAMES} frames (~{MAX_FRAMES * 0.1:.0f} seconds)")
    print("Or press Ctrl+C to stop early")
    print("\nStarting in 3 seconds...")
    
    time.sleep(3)
    
    frame_count = 0
    
    try:
        while frame_count < MAX_FRAMES:
            frame_count += 1
            
            img = capture_game_region()
            obstacle_distance = detect_obstacles_debug(img)
            
            if obstacle_distance:
                if obstacle_distance <= JUMP_THRESHOLD:
                    print(f"Frame {frame_count}/{MAX_FRAMES}: JUMP at {obstacle_distance}px")
                else:
                    print(f"Frame {frame_count}/{MAX_FRAMES}: SAFE - {obstacle_distance}px away")
            else:
                print(f"Frame {frame_count}/{MAX_FRAMES}: No obstacles")
            
            time.sleep(0.1)
        
        print(f"\n✅ Completed {MAX_FRAMES} frames!")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped early!")
    
    finally:
        cv2.destroyAllWindows()
        print(f"\nTotal frames processed: {frame_count}")

if __name__ == "__main__":
    play_game_debug()