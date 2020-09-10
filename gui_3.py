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
from tinydb import Query

from frames import Tab, FilesFrame, PathsFrame
from gui_4 import HomeFirstTime, HomeWalletImport, Home
from tools import *
from managers import *
from server import Server
import db
import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.threaded import pool

from wallet import WalletFrame


class Header(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        # Header config
        resp_grid(self, 1, 5)
        self.configure(width=self.master['width'])
        self.server = Server(self)
        # self.main = Background(widget=self, sticky="n",
        #            img_path=r'C:\Users\IOPDG\Desktop\img\epiclogo.png').bg_label.grid(row=0, columnspan=5)

        # Header Widgets
        self.status_label = tk.Label(self, text="Node Server: ")
        self.status_info = tk.Label(self, textvariable=self.server.status)
        self.status_info.config(fg=get_color(self.server.status.get()))

        # Header Grid
        self.status_label.grid(row=0, column=0, sticky="e")
        self.status_info.grid(row=0, column=1, sticky="w")
        self.server.button.grid(row=0, column=4)
        self.server.sync.grid(row=0, column=3)

    def change_color(self):
        self.status_info.config(fg=get_color(self.server.status.get()))


class Body(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        # Body config
        # self.bg_img = r'C:\epic-tools\img\bg_first_time.png'
        self.configure(bg="brown", width=self.master['width'], borderwidth=0)
        # self.bg = Background(self, img_path=self.bg_img)
        resp_grid(self, 1, 1)

        # # Body Widgets
        # self.navbar = Tab(self, height=550)
        # self.page0 = tk.Frame(self, bg="red")
        # self.page1 = tk.Frame(self, bg="green")
        # self.page2 = tk.Frame(self, bg="gold")
        #
        # # Body Grid
        # self.navbar.add(self.page0, text=f'red')
        # self.navbar.add(self.page1, text=f'green')
        # self.navbar.add(self.page2, text=f'gold')
        # self.navbar.grid(row=0, column=0, sticky="new",
        #                  ipady=10, ipadx=10)

        # Body Widgets
        # self.bg.bg_label.grid()
        self.first_time = HomeFirstTime(self, borderwidth=0)
        self.home = Home(self, borderwidth=0)

        # Body Grid
        if db.users.all()[0]['first_run']:
            self.first_time.grid(row=0, column=0, sticky="news")
            # db.users.update({"first_run": False})
        else:
            self.home.grid(row=0, column=0, sticky="news")


class Footer(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.configure(bg="brown")

        self.width_label = tk.Label(self, text='Width:')
        self.entry_W = tk.Entry(self, background="pink")

        self.entry_W.grid(row=0, column=1)
        self.width_label.grid(row=0, column=0)
