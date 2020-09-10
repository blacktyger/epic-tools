import queue
import threading
from subprocess import Popen, PIPE
from threading import Thread
import multiprocessing
from tkinter import ttk
import time
from tkinter import filedialog, Text
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

from PIL import Image, ImageTk
from tools import *
from managers import *
from gui_3 import *
import db
import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.threaded import pool


class HomeFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        # Root configuration (layer 1)
        self.master.title('Epic-Cash tools')
        self.master.geometry(self.set_size(root=True))
        self.master.config(bg="black", width=self.set_size()[0],
                           height=self.set_size()[1], borderwidth=0)
        # self.master.resizable(width=False, height=False)
        resp_grid(self.master, 1, 1)

        # HomeFrame configuration (layer 2)
        self.config(width=self.set_size()[0],
                    height=self.set_size()[1],
                    bg="black", borderwidth=0)
        self.columnconfigure(0, minsize=500, weight=1)
        self.grid_rowconfigure(0, minsize=50, weight=1)
        self.grid_rowconfigure(1, minsize=750, weight=1)
        self.grid_rowconfigure(2, minsize=50, weight=1)
        self.grid(sticky="nswe")

        # Frames in HomeFrame (layer 3)
        self.header = Header(self, borderwidth=0)
        self.body = Body(self, borderwidth=0)
        self.footer = Footer(self, borderwidth=0)
        self.header.grid(row=0, sticky="news")
        self.body.grid(row=1, sticky="news")
        self.footer.grid(row=2, sticky="ews")

    def set_size(self, root=False, app_width=500, app_height=800):
        screen_height = self.master.winfo_screenheight()
        screen_width = self.master.winfo_screenwidth()
        print(f"SCREEN SIZE {screen_width}x{screen_height}")
        if root:
            return f"{app_width}x{screen_height -200}+{screen_width - (app_width + 20)}+0"
        return app_width, app_height


root = tk.Tk()
app = HomeFrame(root)
app.mainloop()
