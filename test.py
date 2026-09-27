import tkinter as tk


def create_window(txt):
    win = tk.Tk()
    win.attributes("-toolwindow", True)
    win.attributes("-alpha", 0.8)
    win.geometry("400x300")
    label = tk.Label(text=txt, font=("Arial", 16), height=3, wraplength=350)
    label.pack()
    win.mainloop()


create_window("dfdfgggdfffffffffffdffghfghfghfgdfgdfgdfgdgdfgdf")
