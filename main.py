import tkinter as tk
import mss
import easyocr
import argostranslate.translate
import numpy
import keyboard

reader = easyocr.Reader(["ru", "en"], gpu=False)


class Screen:
    def __init__(self):
        self.root = tk.Tk()
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

        self.root.mainloop()

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
    win = tk.Tk()
    win.attributes("-toolwindow", True)
    
    win.geometry("400x300")
    label = tk.Label(text=txt, font=("Arial", 16), wraplength=350)
    label.pack()
    win.mainloop()

def translate(text):
    if not text.strip():
        return ""
    from_code = "en"
    to_code = "ru"

    translated_text = argostranslate.translate.translate(text, from_code, to_code)
    return translated_text




def main():
    realisation = Screen()

    region = realisation.get_region()

    if region:
        with mss.MSS() as sct:
            screenshot = sct.grab(region)
            img_np = numpy.array(screenshot)
        result = reader.readtext(img_np, detail=0)
        result = " ".join(result)

        
        russian_text = translate(result)
        
        create_window(russian_text)





keyboard.add_hotkey("shift+u", main)
keyboard.wait("shift+i")
