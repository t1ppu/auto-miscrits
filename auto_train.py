import sys
import pyautogui
import pytesseract
import easyocr
from PIL import Image, ImageFilter, ImageOps, ImageGrab
import time
from plyer import notification  # Import the notification library
import winsound
import numpy as np
import requests
import win32gui
import win32api
import win32con
from ctypes import windll
import win32ui

pyautogui.FAILSAFE = False

###############################
plat1 = True
plat2 = True
plat3 = True
plat4 = True
c1, c2 = 961, 506 # use mouse.py to get coordinates of the target search object
miscrits_to_avoid = {"Quebble"} 
time_gap = 5

# List of common Miscrits to skip
common_miscrits = {"Peekly", "Owlie", "Owlle", "Fells", "Felis", "Flue", "Whik", "Flowerplller", "Flowerpiller", "Prawnja", "Flurfy", "Sparkupine", "Hydroseal", "Cubsprout", "Cubspr", "Flowerp", "Futy", "Flurty", "Whlk", "Sparkuplne",  "Flamellng", "Lumera", "Squlrmle", "Snortus", "Qulrk", "Snatcher", "Elefauna", "Nessy", "Hotfoot", 'Steamguln', 'Twlggum', "Squlbee", 'Crlckln', "Shellbee", "Vhlsp", "Statlkat", "Bubbles", "Arla", "Cerber", "Raldio", "Tongutall", "Frostmlte", "Craggy", "Croaky","Nero", "Sparkspeck", "Raldlo", "Ratlery", "Railery", "Sllthero", "Lavarllla", "Auger", "Vexie", "Vexle", "Jellyshock", "Sparkslug", "Hlppoke", "Quebble", "Tectonyx", "Hawkal", "Dlgsy", "Weevern", "Orca", "Leggy", "Blub", "Zaptor", "Spark", "Echlno", "Grub", "Wavesllng", "Jack", "Nlbbles", "Arlgato", "Dlgsy", "Nlbbles", "Nibbles", "Craggy", "Hottoot", "Rallery", "Bludger", "Plllblaze" }

rare = {"3","3h", "3l", "Dark", "klloray", "kiloray", "Bll", "Blighted Cubsprout", "Bllghted cubsprout", "Bllghfed cubsprout", "Blighted cubzprout", "Bllghted cubzsprout", "3hahted cubarett", "3hhted cubarett", "Freedom", "Free", "Papa", "Flender", "Deflllo", "Kelpa", "Dorux", "Thundercracker", "Thunder", "Kelpe", "Foll", "Meme", "Gog", "Foil", "Tullp", "Derk", "Llght", "Light", "Licht", "Mama", "Nana", "Blazertooth", "Blaze", "Flarlng", "Dorux", "Keeper", "Gemlx" }


ready = {"READYOTRAIN", "RBADYTOTRAIN", "READYIOTRAIN", " READYOTRAIN", " RBADYTOTRAIN", " READYIOTRAIN", "READYTOTRAIN", " READYTOTRAIN"}
############################### 

# Identify the target window by title
window_title = "Miscrits (DEBUG)"  # Replace with the title of your target window
hwnd = win32gui.FindWindow(None, window_title)
# print(hwnd)
if not hwnd:
    print(f"No window found with title '{window_title}'")
    exit()
    
# Pushover setup
pushover_token = ''  # Replace with your Pushover app token
pushover_user_key = ''  # Replace with your Pushover user key

# Initialize the easyocr reader
reader = easyocr.Reader(['en'])
time.sleep(3)

# Function to detect text in a region
def detect_text(r):
    image = pyautogui.screenshot(region=r)
    image = ImageOps.grayscale(image)
    image = image.filter(ImageFilter.SHARPEN)
    image_np = np.array(image)
    result = reader.readtext(image_np)
    detected_text = ' '.join([text[1] for text in result]).strip()
    return detected_text

# Screenshot the target window
def screenshot():
  w = 1920
  h = 1080

  hwndDC = win32gui.GetWindowDC(hwnd)
  mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
  saveDC = mfcDC.CreateCompatibleDC()

  saveBitMap = win32ui.CreateBitmap()
  saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

  saveDC.SelectObject(saveBitMap)

  # Change the line below depending on whether you want the whole window
  # or just the client area. 
  #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
  result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)

  bmpinfo = saveBitMap.GetInfo()
  bmpstr = saveBitMap.GetBitmapBits(True)

  im = Image.frombuffer(
      'RGB',
      (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
      bmpstr, 'raw', 'BGRX', 0, 1)

  win32gui.DeleteObject(saveBitMap.GetHandle())
  saveDC.DeleteDC()
  mfcDC.DeleteDC()
  win32gui.ReleaseDC(hwnd, hwndDC)
  return im

# Function to send a click event to a background window
def click_in_window(hwnd, x, y):
    # x, y = win32gui.ClientToScreen(hwnd, (x, y))
    lParam = win32api.MAKELONG(x, y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    time.sleep(0.1)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)
    # win32gui.SendMessage(hwnd, win32con.WM_MOUSEMOVE, None, lParam)
    
def send_pushover_notification(title, message):
    payload = {
        'token': pushover_token,
        'user': pushover_user_key,
        'title': title,
        'message': message
    }
    try:
        response = requests.post("https://api.pushover.net/1/messages.json", data=payload)
        if response.status_code == 200:
            print("Pushover notification sent successfully!")
        else:
            print(f"Failed to send Pushover notification: {response.status_code}")
    except Exception as e:
        print(f"Error sending Pushover notification: {e}")

def train_miscrit(n):
    pl = False
    if n==1 and plat1:
      pl = True
    elif n==2 and plat2:
      pl = True
    elif n==3 and plat3:
      pl = True
    if pl:
      print("Plat train")
    time.sleep(1)
    if n==1:
      print("train miscrit 1")
    elif n==2:
      print("train miscrit 2")
    elif n==3:
      print("train miscrit 3")
    elif n==4:
      print("train miscrit 4")
    # click_in_window(hwnd, x=185, y=80) # open train
    pyautogui.click(x=449, y=69)
    time.sleep(2)
    if n==2:
      pyautogui.click(x=729, y=342)
    elif n==3:
      pyautogui.click(x=735, y=391)
    elif n==4:
      pyautogui.click(x=745, y=453)
    time.sleep(2)
    ###### click train
    pyautogui.click(x=998, y=253)
    time.sleep(2)
    if plat1:
      pyautogui.click(x=881, y=825) ## plat train
      time.sleep(1)
      pyautogui.click(x=1113, y=826) ## continue
      time.sleep(2)
    ####### click continue twice
    else:
      pyautogui.click(x=1113, y=826)
      time.sleep(1)
      pyautogui.click(x=1113, y=826)
      time.sleep(2)
    ######## new move or evolution or both
    detected_text = detect_text((910,621,102,27))
    print("new move? ->" + detected_text)
    if detected_text == "Contlnue" or detected_text == "ontive" or detected_text == "Sontlua":
      print("new move")
      pyautogui.click(x=950, y=632)
      time.sleep(1)
    #### evolution
    detected_text = detect_text((908,750,102,27))
    print("new evo? ->" + detected_text)
    if detected_text == "Contlnue" or detected_text == "@ontlug" or detected_text == "Eontinue":
      print("evolution")
      pyautogui.click(x=950, y=762)
      time.sleep(1)
    #### skip if level up:
    detected_text = detect_text((929, 709, 64, 20))
    print("level up? ->" + detected_text)
    if detected_text == "Sklp" or detected_text == "sklp" or detected_text == "Skip" or detected_text == "Skp":
      print("level up")
      pyautogui.click(x=960, y=717)
      time.sleep(1)
    ####### close train menu
    pyautogui.click(x=1313, y=225)
    print("CLOSED TRAIN MENU")
    time.sleep(1)

## AFTER THE BATTLE STARTS
# Define the region where the Miscrit's name appears 
# (adjust these coordinates)
name_left, name_top, name_right, name_bottom = 1169, 68, 79, 20

# Coordinates of the "man running" button
exit_x, exit_y = 606, 865  # Example coordinates

count = 0
# Start an infinite loop to continuously check the screen
while True:
    f = False
    g = False
    av = False
    pyautogui.click(x=c1, y=c2)
    # click_in_window(hwnd, x=974, y=435)
    print("Searching...")
    time.sleep(6.5)
    # Capture the region where the Miscrit's name appears
    name_region = (name_left, name_top, name_right, name_bottom)
    name_image = pyautogui.screenshot(region=name_region)
    # name_image.show()
    # print(name_image)
    name_image = ImageOps.grayscale(name_image)
    name_image = name_image.filter(ImageFilter.SHARPEN)
    name_image_np = np.array(name_image)
    # name_image.save(f'C:/Users/kolli/OneDrive/Desktop/finds/miscrit{count}.png')
    
    # Use easyocr to extract the text from the name region
    result = reader.readtext(name_image_np)
    detected_text = ' '.join([text[1] for text in result]).strip()
    print(detected_text)
    
    for r in rare:
          if r in detected_text:
            f = True
            print(f"Detected rare Miscrit: {r}. Sending notification.")
            # Play a sound
            winsound.Beep(1000, 1500)  # Frequency in Hz, Duration in milliseconds
            # Send a desktop notification
            notification.notify(
                title="Rare Miscrit Detected!",
                message=f"You encountered a rare Miscrit: {r}.",
                timeout=10  # Duration the notification stays on the screen (in seconds)
            )
            send_pushover_notification("Rare Miscrit Detected!", f"You encountered a rare Miscrit: {r}.")
            print("User notified")
            input("Press Enter to continue...")
            time.sleep(3)
            break
    # Check if the detected Miscrit is common
        # Check if the detected Miscrit is the rare one
    for mi in miscrits_to_avoid:
      if mi in detected_text:
        av = True
        print(f"Detected common Miscrit to avoid: {mi}. Exiting the battle.")
        # click_in_window(hwnd, x=exit_x, y=exit_y)
        pyautogui.click(x=exit_x, y=exit_y)
        time.sleep(3.5)
        print("Closing")
        # click_in_window(hwnd, x=963, y=753)
        pyautogui.click(x=963, y=753)
        break
        
    if not f and not av:
      for miscrit in common_miscrits:
          if miscrit in detected_text:
              g = True
              print(miscrit, detected_text)
              print(f"Detected common Miscrit: {miscrit}")          
              pyautogui.click(x=710, y=955) # 1st slot attack
              # pyautogui.click(x=882, y=955) # 2st slot
              # pyautogui.click(x=1050, y=955) # 3st slot
              # pyautogui.click(x=1200, y=955) # 4st slot
              
              print("Fighting with best attack")
              time.sleep(12)
              while True:     ### attack until battle ends
                detected_text1 = detect_text(name_region)
                if detected_text1 in common_miscrits:
                  pyautogui.click(x=710, y=955) # 1st slot attack
                  # pyautogui.click(x=882, y=955) # 2st slot
                  # pyautogui.click(x=1050, y=955) # 3st slot
                  # pyautogui.click(x=1200, y=955) # 4st slot
                  time.sleep(10)
                else:
                  break
              
              ######## check if miscrit ready to train
              
              w = detect_text((660, 438, 103, 21))    ## 1st miscrit
              x = detect_text((810, 440, 103, 21))    ## 2nd miscrit
              y = detect_text((673, 535, 103, 21))    ## 3rd miscrit
              z = detect_text((817, 533, 103, 21))    ## 4th miscrit
              print("Battle end. Closing")
              # click_in_window(hwnd, x=965, y=756) #close
              pyautogui.click(x=965, y=756)
              time.sleep(1)
              if w in ready:
                train_miscrit(1)
              if x in ready:
                train_miscrit(2)
              if y in ready:
                train_miscrit(3)
              if z in ready:
                train_miscrit(4)
              time.sleep(time_gap)
              break
            
    if not g and not f and not av:
      detected_text = detect_text((1652, 75, 100, 30))
      print("heal?", detected_text)
      if "Heal" in detected_text:
        print("gold(?)")
        time.sleep(20)
      else:
        print("Found something or game stuck")
        # Play a sound
        winsound.Beep(1000, 1500)  # Frequency in Hz, Duration in milliseconds
        # Send a desktop notification
        notification.notify(
            title="Found something",
            message=f"zzzz",
            timeout=10  # Duration the notification stays on the screen (in seconds)
        )
        send_pushover_notification("Found something", f"zzzz")
        input("Press Enter to continue...")
        time.sleep(3)
        
    # heal if dead
    dead_region = (110, 65, 20, 20) #1st slot
    # dead_region = (170, 65, 20, 20) #2nd slot
    dead_image = pyautogui.screenshot(region=dead_region)
    dead_image_np = np.array(dead_image)
    is_grayscale = np.all(dead_image_np[..., 0] == dead_image_np[..., 1]) and np.all(dead_image_np[..., 1] == dead_image_np[..., 2])   
    if is_grayscale:
      pyautogui.click(x=1700, y=90) 
    # pyautogui.move(1, 0)
    print(count)
    count += 1
    # Wait for 30 seconds before checking again
