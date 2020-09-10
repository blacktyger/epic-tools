from tkinter import ttk
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, Text
from PIL import Image, ImageTk
from frames import *
import os
from distutils.dir_util import copy_tree
from tkinter.scrolledtext import ScrolledText
from check_process import Program, Command, process_manager, check_process


class HomeFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.frame = parent

        resp_grid(self.frame, 3, 1)

        self.frame.title('Epic-Cash tools')
        self.frame.geometry('700x700')

        self.top_frame = Header(root, bg='black', width=450, height=250, pady=3)
        self.center = Body(root, bg='gray2', padx=3, pady=3)
        self.btm_frame = Footer(root, bg='white', width=450, height=45, pady=3)

        self.top_frame.grid(row=0, sticky="nsew")
        self.center.grid(row=1, sticky="nsew")
        self.btm_frame.grid(row=3, sticky="ew")


root = tk.Tk()
app = HomeFrame(root)
app.mainloop()


