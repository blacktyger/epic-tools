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
        # resp_grid(self, 2, 1)
        self.bg_img = tk.PhotoImage(file=r'C:\epic-tools\img\bg7.png')
        self.label_area = tk.Canvas(self, width=500, height=40, borderwidth=0,
                                    highlightthickness=0, bg='black')
        self.btns_area = tk.Canvas(self, width=500, height=800, borderwidth=0,
                                   highlightthickness=0)

        self.columnconfigure(0, minsize=500, weight=1)
        self.grid_rowconfigure(0, minsize=50, weight=1)
        self.grid_rowconfigure(1, minsize=750, weight=1)

        # HomeFirstTime Widgets
        self.wallet = Wallet(master=self, login_redirect=HomeWalletImport(master=self))
        self.wallet_import = HomeWalletImport(self.btns_area)
        self.label_area.grid(sticky="news")
        self.btns_area.grid(sticky="news")
        self.btns_area.create_image(0, 0, image=self.bg_img, anchor='nw')

        self.create_wallet_btn = tk.Button(self.btns_area, bg="#e6b800",
                                           borderwidth=1,
                                           text="Create New Wallet",
                                           command=self.run_wallet)
        self.import_wallet_btn = tk.Button(self.btns_area, bg="#e6b800",
                                           borderwidth=1,
                                           text="Import Wallet",
                                           command=self.import_command)

        if self.scan_for_seed():
            # EXISTING WALLET LOGIN
            # self.btns_area.create_text(250, 150, fill="white", font="Times 20 bold",
            #                            text="LOGIN TO WALLET")
            self.pass_input = self.wallet.password_input(widget=self.btns_area)
            self.pass_btn = self.wallet.send_password_btn(widget=self.btns_area, bg="gold")

            self.btns_area.create_window(int(self.btns_area['width']) / 2, 410,
                                         window=self.pass_input, height=40, width=380)
            self.btns_area.create_window(int(self.btns_area['width']) / 2, 500,
                                         window=self.pass_btn, height=34, width=300)

            self.pass_info = self.btns_area.create_text(int(self.btns_area['width']) / 2, 445,
                                                        fill="white", font="Helvetica 11 bold",
                                                        text="Please provide wallet password")
            self.btns_area.create_window(150, 700,
                                         window=self.create_wallet_btn, height=25, width=150)
            self.btns_area.create_window(350, 700,
                                         window=self.import_wallet_btn, height=25, width=150)

        else:
            # NO WALLET SEED SCREEN Grid
            self.import_wallet_btn.grid(row=0, column=0, ipady=10,
                                        padx=40, ipadx=150, pady=420, sticky="new")
            self.create_wallet_btn.grid(row=0, column=0, ipady=10,
                                        padx=40, pady=250, ipadx=150, sticky="new")

    def scan_for_seed(self):
        user = os.getlogin()
        file = "wallet.seed"
        default_path = fr"C:\Users\{user}\.epic\main\wallet_data\{file}"

        if os.path.exists(default_path):
            return True
        else:
            return False

    def import_command(self):
        self.btns_area.delete('all')
        # self.import_wallet_btn.destroy()
        # self.create_wallet_btn.destroy()
        # self.pass_input.destroy()
        # self.pass_info.destroy()
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
        self.wallet = Wallet(master=self)
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
