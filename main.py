import os
import sys
import threading
import tkinter as tk
import mss
import easyocr
import numpy
from pynput import keyboard
from googletrans import Translator
import pystray
from PIL import Image

reader = None
def get_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(["ru", "en"], gpu=False)
    return reader

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

root = tk.Tk()
root.withdraw()

class Screen:
    def __init__(self):
        self.root = tk.Toplevel(root)
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.4)
        self.root.attributes("-topmost", True)
        
        self.x = 0
        self.y = 0
        self.end_x = 0
        self.end_y = 0
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=1)
        self.canvas.bind("<Button-1>", self.pressed)
        self.canvas.bind("<B1-Motion>", self.motion)
        self.canvas.bind("<ButtonRelease-1>", self.pressed_release)

        self.rect = self.canvas.create_rectangle(0, 0, 0, 0, outline="red", width=2)
        
        self.root.wait_window()

    def pressed(self, event):
        self.x = event.x
        self.y = event.y
        self.canvas.coords(self.rect, self.x, self.y, self.x, self.y)

    def motion(self, event):
        cur_x = event.x
        cur_y = event.y
        self.canvas.coords(self.rect, self.x, self.y, cur_x, cur_y)

    def pressed_release(self, event):
        self.end_x = event.x
        self.end_y = event.y

        self.root.destroy()

    def get_region(self):
        top = min(self.y, self.end_y)
        left = min(self.x, self.end_x)
        width = abs(self.end_x - self.x)
        height = abs(self.end_y - self.y)
        region = {"top": top, "left": left, "width": width, "height": height}
        if width == 0 or height == 0:
            return None
        return region


def create_window(txt):
    win = tk.Toplevel(root)
    win.title("Перевод")
    win.attributes("-toolwindow", True)
    win.attributes("-topmost", True)
    
    label = tk.Label(win, text=txt, font=("Arial", 14), wraplength=380, padx=15, pady=15)
    label.pack(expand=True, fill="both")


def translate(text):
    
    translator = Translator()
    translated = translator.translate(text, src="en", dest="ru")
    return translated.text

def do_translate(region):
    with mss.MSS() as sct:
        screenshot = sct.grab(region)
        img_np = numpy.array(screenshot)
    ocr = get_reader()
    result = ocr.readtext(img_np, detail=0)
    result = " ".join(result)

    russian_text = translate(result)

    root.after(0, create_window, russian_text)


def main():
    realisation = Screen()
    region = realisation.get_region()
    if region:
        trey_thread_tarslate = threading.Thread(target=do_translate, args=(region,), daemon=True)
        trey_thread_tarslate.start()



def on_quit(icon, item):
    icon.stop()
    root.after(0, root.destroy)
    os._exit(0)


def setup_tray():
    
    app_icon = Image.open(resource_path("icon.ico"))
    icon = pystray.Icon(
        "TestApp",
        app_icon,
        "TestApp",
        menu=pystray.Menu(pystray.MenuItem("Выход", on_quit)),
    )
    icon.run()


trey_thread_ico = threading.Thread(target=setup_tray, daemon=True)
trey_thread_ico.start()


hotkey = keyboard.GlobalHotKeys({
    "<shift>+u": lambda: root.after(0, main), 
    "<shift>+г": lambda: root.after(0, main)})
hotkey.start()
root.mainloop()
