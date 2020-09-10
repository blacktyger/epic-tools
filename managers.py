from tools import *
from tkinter import ttk
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, Text
from PIL import Image, ImageTk


class Background:
    """
    Class that helps with background images inside frames. Files are resized
    to tk.Frame size (keeping ratio) and tk.Label have same bg colour as parent tk.Frame
    :widget - working tk.Frame instance
    :img_path - path to background image
    """

    def __init__(self, widget, img_path, sticky='wesn'):
        self.widget = widget
        self.img_path = img_path
        self.img = self.resize()
        self.bg_label = tk.Label(self.widget, image=self.img, bg=self.widget['bg'])
        self.bg_label.image = self.img

    def resize(self):
        print(f"From BG Class: {self.widget['width']} {self.widget['height']}")
        img = Image.open(self.img_path)
        width = self.widget['width']
        percent = (width / float(img.size[0]))
        height = int((float(img.size[1]) * float(percent)))
        bg = img.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(bg)


class FileManager:
    """
    Manager for files used in program;
    :widget - tk.Entry instance where path will be shown
    """

    def __init__(self, widget, name):
        self.widget = widget
        self.name = name

    def add_file(self):
        path = filedialog.askopenfilename(
            initialdir=r"C:\Users\IOPDG\Desktop\Mining stuff", title=f"Select path to {self.name}",
            filetypes=(("exec files", "*.exe"), ("bat files", "*.bat")))
        if path:
            self.widget.delete(0, tk.END)
            self.widget.insert(0, path)
            return path
        else:
            pass

    def file_path(self):
        path = filedialog.askopenfilename(
            initialdir=r"C:\Users\IOPDG\Desktop\Mining stuff", title=f"Select path to {self.name}",
            filetypes=(("exec files", "*.exe"), ("bat files", "*.bat")))
        return fr"{path}"


class Button:
    """
    Manager for creating tk.Button - tk.Entry pairs;
    :widget - tk.Entry instance where path will be shown
    """

    def __init__(self, widget, name, text, command, grid=[0, 0], sticky=s['x'], *args, **kwargs):
        self.widget = widget
        self.text = text
        self.sticky = sticky
        self.name = name
        # self.entry = tk.Entry(self.widget, background="pink", width=35)
        self.command = command
        self.button = tk.Button(
            self.widget, text=self.text, command=self.command,
            padx=3, pady=2, fg='black', bg='white')

        # self.entry.insert(0, f'<--- Select  {self.name} path')  # join ^
        # self.entry.grid(row=grid[0], column=grid[1]+1, sticky=self.sticky,
                        # padx=2, ipady=4)
        self.button.grid(row=grid[0], column=grid[1], sticky=self.sticky,
                         padx=5, pady=5)


class ButtonEntry:
    """
    Manager for creating tk.Button - tk.Entry pairs;
    :widget - tk.Entry instance where path will be shown
    """

    def __init__(self, widget, name, grid=[0, 0], sticky=s['x'], *args, **kwargs):
        self.widget = widget
        self.sticky = sticky
        self.name = name
        self.entry = tk.Entry(self.widget, background="pink", width=35)
        self.command = FileManager(self.entry, name=f"{self.name}")
        self.button = tk.Button(
            self.widget, text=f" {self.name.lower()} path",
            command=lambda: self.command.add_file(),
            padx=3, pady=2, fg='black', bg='white')

        self.entry.insert(0, f'<--- Select  {self.name} path')  # join ^
        self.entry.grid(row=grid[0], column=grid[1]+1, sticky=self.sticky,
                        padx=2, ipady=4)
        self.button.grid(row=grid[0], column=grid[1], sticky=self.sticky,
                         padx=5, pady=5)

