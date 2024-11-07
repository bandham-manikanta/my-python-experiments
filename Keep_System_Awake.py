import pyautogui
import time
import datetime
import requests

pyautogui.FAILSAFE = False

def get_encouraging_message():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        data = response.json()
        if data:
            return data[0]['q'] + " - " + data[0]['a']
    except Exception as e:
        print("Error fetching encouraging message:", e)
    return None

print('\nAgent is active.\n')

def press_shift():
    for i in range(3):
        pyautogui.press('shift')
        pyautogui.press('shift')
        time.sleep(1)

# Function to check if the time is 01 second of every five minutes
def is_one_second_of_ten_minutes():
    now = datetime.datetime.now()
    if now.second == 1 and now.minute % 30 == 0:
        return True
    return False

while True:
    press_shift()
    time.sleep(30)
    if is_one_second_of_ten_minutes():
        encouraging_message = get_encouraging_message()
        if encouraging_message:
            print(encouraging_message, "\n\n")
