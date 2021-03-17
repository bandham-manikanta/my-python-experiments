import pyautogui as gui

import time

gui.FAILSAFE = False

while True:
    time.sleep(10)
    for i in range(0, 10):
        gui.moveTo(0, i*5)
    for i in range(0, 3):
        gui.press('shift')