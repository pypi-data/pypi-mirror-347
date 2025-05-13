import pyautogui
import keyboard
import time

class TrackMousePosition():
    def __init__(self):
        pass

    def mousePosition(self):
        print("Press the 'Enter' key to quit.")

        while not keyboard.is_pressed('Enter'):
            x, y = pyautogui.position()

            position = f'X: {x:4} Y:{y:4}' 

            print(position, end='')
            print(end='\r', flush=True)
            time.sleep(0.1)

        print('\n Program has exited.')
