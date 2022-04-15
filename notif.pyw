from tkinter import *
import pyautogui
import time

def __init__(string):
    width, height= pyautogui.size()
    root = Tk()
    window = Canvas(root)
    root.geometry(f"250x75+{width - 250}+0")
    root.overrideredirect(1)
    root.attributes("-topmost", True)
    root.resizable(0,0)
    text = LabelFrame(root, text="Now playing:", fg="white", bg="gold", width="250", height="75",bd=2).place(x=0, y=0)
    song = LabelFrame(text, text=string[0:22] + "...", fg="white",bg="gold",font=("consolas", 12,"bold"), width="230", height="30", bd=0).place(x=10, y=35)

    root.update()

    time.sleep(5)
    root.destroy()