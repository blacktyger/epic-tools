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

from frames import Tab, FilesFrame, PathsFrame
from tools import *
from managers import *
from server import Server
from db import *
import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.threaded import pool

from wallet import WalletFrame, Wallet


class HomeFirstTime(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        # HomeFirstTime config
        resp_grid(self, 1, 1)
        self.bg_img = tk.PhotoImage(file=r'C:\epic-tools\img\bg7.png')
        self.btns_area = tk.Canvas(self, width=450, borderwidth=0,
                                   highlightthickness=0)

        # HomeFirstTime Widgets
        self.wallet_import = HomeWalletImport(self.btns_area)
        self.create_wallet_btn = tk.Button(self.btns_area, bg="#e6b800",
                                           borderwidth=1,
                                           text="Create New Wallet",
                                           command=self.run_wallet)
        self.import_wallet_btn = tk.Button(self.btns_area, bg="#e6b800",
                                           borderwidth=1,
                                           text="Import Wallet",
                                           command=self.import_command)

        # HomeFirstTime Grid
        self.btns_area.grid(sticky="new")
        self.btns_area.create_image(0, 0, image=self.bg_img, anchor='nw')
        self.import_wallet_btn.grid(row=0, column=0, ipady=10,
                                    padx=40, ipadx=150, pady=420, sticky="new")
        self.create_wallet_btn.grid(row=0, column=0, ipady=10,
                                    padx=40, pady=490, ipadx=150, sticky="new")

    def import_command(self):
        self.import_wallet_btn.destroy()
        self.create_wallet_btn.destroy()
        self.wallet_import.grid(row=0, column=0, sticky="news")

    def run_wallet(self):
        # if self.master.header.server.status == "Online":
        new_window = tk.Toplevel(self)
        self.wallet_window = WalletFrame(new_window)
        self.wallet_window.master.geometry('770x600+680+0')
        resp_grid(self.wallet_window, 2, 2)
        self.wallet_window.grid(sticky="nswe")


class Home(HomeFirstTime):
    def __init__(self, master, *args, **kwargs):
        HomeFirstTime.__init__(self, master, *args, **kwargs)

        self.bg_img = tk.PhotoImage(file=r'C:\epic-tools\img\bg6.png')
        self.btns_area.create_image(0, 0, image=self.bg_img, anchor='nw')


class HomeWalletImport(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        # HomeFirstTime config
        resp_grid(self, 1, 1)
        # self['bg'] = "red"
        self.wallet = Wallet(password="majkut11")
        self.bg_img = tk.PhotoImage(file=r'C:\epic-tools\img\bg7.png')
        self.btns_area = tk.Canvas(self, width=500, height=780, borderwidth=0,
                                   highlightthickness=0, bg="white")
        self.btns_area.create_image(0, 0, image=self.bg_img, anchor='nw')
        self.seed_file = tk.Button(self.btns_area, bg="#e6b800",
                                   borderwidth=1,
                                   text="Import from seed file",
                                   command=self.wallet.get_seed_file)
        self.seed_phrase = tk.Button(self.btns_area, bg="#e6b800",
                                     borderwidth=1,
                                     text="Import from mnemonic seed phrase",
                                     command=self.import_phrase)

        self.btns_area.grid(sticky="nswe")
        self.seed_file.grid(row=0, column=0, ipady=10,
                            padx=40, ipadx=150, pady=420, sticky="new")
        self.seed_phrase.grid(row=0, column=0, ipady=10,
                              padx=40, ipadx=120, pady=490, sticky="new")

    def import_seed(self):
        pass

    def import_phrase(self):
        pass
