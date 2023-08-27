import pyautogui
import pytesseract as tess
import keyboard
import time
import os
import tkinter as tk
import pyperclip
from tkinter import ttk
from PIL import Image

#you need tesseract installed for this code to work
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

stop_typing_flag = False

def on_stop_button_click():
    global stop_typing_flag
    stop_typing_flag = True
    run_button.config(state=tk.NORMAL)
    custom_run_button.config(state=tk.NORMAL)
    copy_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

def stop_typing_with_shortcut():
    on_stop_button_click()

def run_ocr_and_typing():
    global stop_typing_flag

    def start_typing():
        screenshot_folder = os.path.expanduser('C:/Users/logan/Pictures/Screenshots')
        screenshot_files = os.listdir(screenshot_folder)
        screenshot_files.sort(key=lambda x: os.path.getmtime(os.path.join(screenshot_folder, x)), reverse=True)
        latest_screenshot = os.path.join(screenshot_folder, screenshot_files[0])

        typing_speed_value = typing_speed.get()
        if typing_speed_value == "0.001":
            typing_delay = 0.001
        elif typing_speed_value == "0.05":
            typing_delay = 0.05
        elif typing_speed_value == "0.025":
            typing_delay = 0.025
        elif typing_speed_value == "0.1":
            typing_delay = 0.1
        else:
            typing_delay = max(0.001, min(1 / max(0.001, float(typing_speed_value)), 0.2))

        screenshot = Image.open(latest_screenshot)
        text = tess.image_to_string(screenshot)

        run_button.config(state=tk.DISABLED)
        custom_run_button.config(state=tk.DISABLED)
        copy_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)

        stop_typing_flag = False

        for char in text:
            if stop_typing_flag:
                break
            if char == '\n':
                keyboard.write(' ')
            else:
                keyboard.write(char)
                time.sleep(typing_delay)

        run_button.config(state=tk.NORMAL)
        custom_run_button.config(state=tk.NORMAL)
        copy_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

    run_button.config(state=tk.DISABLED)
    custom_run_button.config(state=tk.DISABLED)
    copy_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    root.after(2000, start_typing)

def screenshot_and_copy():
    screenshot_folder = os.path.expanduser('C:/Users/logan/Pictures/Screenshots')#where you screenshots go when you do windows shift s
    screenshot_files = os.listdir(screenshot_folder)
    screenshot_files.sort(key=lambda x: os.path.getmtime(os.path.join(screenshot_folder, x)), reverse=True)
    latest_screenshot = os.path.join(screenshot_folder, screenshot_files[0])

    screenshot = Image.open(latest_screenshot)
    text = tess.image_to_string(screenshot)
    pyperclip.copy(text)

def run_custom_text():
    text_to_type = text_box.get("1.0", tk.END).strip()

    def start_typing_custom_text():
        typing_speed_value = typing_speed.get()
        if typing_speed_value == "0.001":
            typing_delay = 0.001
        elif typing_speed_value == "0.05":
            typing_delay = 0.05
        elif typing_speed_value == "0.025":
            typing_delay = 0.025
        elif typing_speed_value == "0.1":
            typing_delay = 0.1
        else:
            typing_delay = max(0.001, min(1 / max(0.001, float(typing_speed_value)), 0.2))

        for char in text_to_type:
            if stop_typing_flag:
                break
            if char == '\n':
                keyboard.write(' ')
            else:
                keyboard.write(char)
                time.sleep(typing_delay)

    run_button.config(state=tk.DISABLED)
    custom_run_button.config(state=tk.DISABLED)
    copy_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    stop_typing_flag = False
    root.after(2000, start_typing_custom_text)

keyboard.add_hotkey('ctrl+y', stop_typing_with_shortcut)

root = tk.Tk()
root.title("Text Typing Bot")

typing_speed = tk.StringVar()
typing_speed.set("0.05")

typing_speed_label = tk.Label(root, text="Typing Speed (characters per second):")
typing_speed_label.pack()

typing_speed_values = ["0.001", "0.05", "0.025", "0.1"]
typing_speed_dropdown = ttk.Combobox(root, textvariable=typing_speed, values=typing_speed_values)
typing_speed_dropdown.pack()

run_button = ttk.Button(root, text="Run from Screenshot", command=run_ocr_and_typing)
run_button.pack()

custom_run_button = ttk.Button(root, text="Run Custom Text", command=run_custom_text)
custom_run_button.pack()

copy_button = ttk.Button(root, text="Copy Text from Last Screenshot", command=screenshot_and_copy)
copy_button.pack()

stop_button = ttk.Button(root, text="Stop", command=on_stop_button_click, state=tk.DISABLED)
stop_button.pack()

text_box = tk.Text(root, height=15, width=70)
text_box.pack()

root.mainloop()
