import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import mss
from PIL import Image
import time

def find_green():
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # Define range for green color in HSV
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    # Convert screenshot to HSV
    hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour
        max_contour = max(contours, key=cv2.contourArea)
        # Get the bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(max_contour)
        # Calculate the centroid of the bounding box
        cx = x + w // 2
        cy = y + h // 2
        # Return the centroid coordinates
        return cx, cy
    else:
        return None

def move_mouse_to_green():
    green_position = find_green()
    if green_position:
        pyautogui.moveTo(green_position[0], green_position[1], duration=0.25)

# Define the color range for player character models
lower_color = np.array([0, 0, 100])   # Lower bound for color (BGR format)
upper_color = np.array([50, 50, 255])  # Upper bound for color (BGR format)

# Main function
def main():
    try:
        # Find the Roblox window
        roblox_windows = gw.getWindowsWithTitle("Roblox")
        if not roblox_windows:
            raise Exception("Error: Roblox window not found.")
        roblox_window = roblox_windows[0]

        # Get the position and size of the Roblox window
        roblox_x, roblox_y, roblox_width, roblox_height = roblox_window.left, roblox_window.top, roblox_window.width, roblox_window.height
        print(f"Roblox window found at ({roblox_x}, {roblox_y}) with width {roblox_width} and height {roblox_height}.")

        with mss.mss() as sct:
            monitor = {"top": roblox_y, "left": roblox_x, "width": roblox_width, "height": roblox_height}

            while True:
                # Capture frame from the screen
                screenshot = sct.grab(monitor)
                frame = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

                # Convert the frame to BGR format for OpenCV
                frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)

                # Convert the frame to HSV color space
                hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                # Threshold the frame to detect player colors
                mask = cv2.inRange(hsv_frame, lower_color, upper_color)

                # Find contours in the mask
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Draw boxes around detected contours (players)
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Display the captured frame with boxes
                cv2.imshow('Roblox ESP', frame)

                # Move mouse to green object
                move_mouse_to_green()

                # Limit frame rate (100 FPS)
                time.sleep(0.01)

                # Check for 'q' key press to exit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close OpenCV windows
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
