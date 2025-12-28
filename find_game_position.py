import mss
import cv2
import numpy as np

print("=" * 60)
print("FINDING GAME WINDOW POSITION")
print("=" * 60)
print("\nThis will capture your ENTIRE screen.")
print("Then you'll click on the game to find its coordinates.")
print("\nStarting in 3 seconds...")
print("Make sure Chrome Dino game is visible!")

import time
time.sleep(3)

# Capture entire screen
with mss.mss() as sct:
    monitor = sct.monitors[1]  # Primary monitor
    screenshot = sct.grab(monitor)
    
    # Convert to numpy array
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    
    print(f"\nScreen size: {img.shape[1]}x{img.shape[0]}")
    print("\nShowing full screenshot...")
    print("INSTRUCTIONS:")
    print("1. Look at the image")
    print("2. Find the Chrome Dino game")
    print("3. Note where it is on your screen")
    print("4. Press any key to close")
    
    # Show full screen
    cv2.imshow('Full Screen Capture', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Now let's help find coordinates
    print("\n" + "=" * 60)
    print("CLICK ON THE GAME TO FIND COORDINATES")
    print("=" * 60)
    print("\nShowing screen again...")
    print("Click on the TOP-LEFT corner of the game area")
    
    coords = []
    
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            coords.append((x, y))
            print(f"Clicked at: X={x}, Y={y}")
            
            # Draw circle where clicked
            cv2.circle(img, (x, y), 10, (0, 255, 0), -1)
            cv2.imshow('Full Screen Capture', img)
            
            if len(coords) == 2:
                print("\nGot both corners! Press any key to continue...")
    
    cv2.imshow('Full Screen Capture', img)
    cv2.setMouseCallback('Full Screen Capture', mouse_callback)
    
    print("\nClick TOP-LEFT corner of game...")
    cv2.waitKey(0)
    
    if len(coords) >= 1:
        print(f"\nClick BOTTOM-RIGHT corner of game...")
        cv2.waitKey(0)
    
    cv2.destroyAllWindows()
    
    if len(coords) >= 2:
        top_left = coords[0]
        bottom_right = coords[1]
        
        width = bottom_right[0] - top_left[0]
        height = bottom_right[1] - top_left[1]
        
        print("\n" + "=" * 60)
        print("COORDINATES FOUND!")
        print("=" * 60)
        print(f"""
Use these values in pixel_agent.py:

monitor = {{
    "top": {top_left[1]},
    "left": {top_left[0]},
    "width": {width},
    "height": {height}
}}
""")
    else:
        print("\nDidn't get both clicks. Run again!")