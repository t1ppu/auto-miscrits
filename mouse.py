import pyautogui
import time
import winsound

# Display the current position of the mouse every second
try:
    while True:
        x, y = pyautogui.position()
        print(f"{x}, {y}")
        time.sleep(1)  # Update every second
except KeyboardInterrupt:
    print("\nExited by user")
