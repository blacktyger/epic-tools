import os
import queue
import threading
from shutil import copy2
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

from tools import *
from managers import *
import db
import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.threaded import pool


class Frame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master


class HeaderFrame(Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        resp_grid(self, 1, 1)
        Background(widget=self, img_path=r'C:\epic-tools\img\wallet.png',
                   sticky='wn')

        # self.label_queue = queue.Queue()
        # self.text = tk.StringVar()
        # self.text.set("Syncing...")
        # self.label = tk.Label(self, textvariable=self.text).grid()
        # self.robot = Robot("robot", self.label_queue, self.node_status)
        # self.updater = LabelUpdater(master=self, name="updater",
        #                             label_queue=self.label_queue,
        #                             variable=self.text)
        # self.updater.start()
        # self.robot.start()

    def node_status(self):
        epic_pass_api_v2 = 'DcxeGBwtZY3FlZcnDFmI'
        r = requests.get('http://localhost:23413/v1/status', auth=('epic', epic_pass_api_v2))
        q = 'Connections: ' + str(r.json()['connections']) + ' Height: ' + str(
            r.json()['tip']['height'])
        self.text.set(q)

        # self.after(1000, self.node_status)


class Wallet:
    def __init__(self, password):
        self.password = password
        self.accounts = ['default']

    def get_seed_file(self):
        print("Clicked!")
        if len(db.file_paths.search(Query()['name'] == "seed")) == 0:
            file_name = filedialog.askopenfilename(
                initialdir=r"C:", title="Select path",
                filetypes=(("all files", "*.*"), ("wallet seed file", "*.seed")))
            db.file_paths.insert({'name': 'seed', 'entry': file_name})
            print(f"{file_name} added to db")
            # copy2(file_name, os.getcwd())
            # return db.file_paths.get(Query()['name'] == "seed")['entry']

    def seed_phrase(self):
        pass

    def get_secret_api(self):
        pass

    def command(self, command):
        cmd = f'epic-wallet -p {self.password} {command}'.split(" ")
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True, bufsize=1)
        stdout, stderr = process.communicate()
        print(stdout, stderr)
        # self.console.screen.insert(tk.END, stdout + '\n' + stderr)
        # self.console.screen.yview(tk.END)
        return process


class Console(Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.var = tk.StringVar()
        self.init_console()

        resp_grid(self, 1, 1)

    def init_console(self):
        self.grid(row=0, column=0, sticky='nswe')
        self.input = tk.Entry(master=self, bg="#7A4545")
        self.input.bind('<Return>', self.send_input)
        self.screen = ScrolledText(master=self, bg="#7A5454")
        self.send_btn = tk.Button(master=self, text="SEND", command=self.send_input)
        self.send_btn.bind('<Return>', self.send_input)

        self.screen.grid(row=0, column=0, sticky="nwes", ipady=3, ipadx=3)
        self.input.grid(row=1, column=0, sticky="nwes", ipady=3, ipadx=3)

    def send_input(self, event=None):
        txt = self.input.get()
        self.save_var(txt)
        self.screen.insert(tk.END, "\n" + txt)
        self.input.delete(0, tk.END)
        self.init_cmd()
        print(self.var.get())

    def save_var(self, text):
        self.var.set(text)

    def get_var(self):
        self.var.get()

    def init_cmd(self):
        self.master.start_thread(func=self.cmd)

    def cmd(self):
        password = "majkut11"
        cmds = f'epic-wallet -p {password} {self.var.get()}'.split(" ")
        proc = Popen(cmds, stdout=PIPE, stderr=PIPE, universal_newlines=True, bufsize=1)
        stdout, stderr = proc.communicate()
        print(stdout, stderr)
        self.screen.insert(tk.END, stdout + '\n' + stderr)
        self.screen.yview(tk.END)
        return proc


class BodyFrame(Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        resp_grid(self, 1, 3)

        # Frames
        self.width_label = tk.Label(self, text=f"")
        # self.width_label.grid(row=1, column=0)
        self.init_buttons()

        self.console = Console(master=self)
        self.console.grid(row=0, column=0, sticky='nswe')

    def init_buttons(self):
        self.buttons = tk.Frame(master=self, bg="red", width=250, height=300)
        self.buttons.grid(row=0, column=1, sticky='nswe')

        self.balance = tk.Button(master=self.buttons, text="Check Balance",
                                 command=self.init_cmd_balance)
        self.balance.grid()
        self.status_btn = tk.Button(master=self.buttons, text="STATUS",
                                    command=self.init_status).grid()
        self.peers_btn = tk.Button(master=self.buttons, text="PEERS",
                                   command=self.init_peers).grid()
        # self.progressbar = tk.Button(master=self.buttons, text="progressbar",
        #                              command=self.init_exec_button_loop)
        # self.progressbar.grid()
        #
        # self.progress = Progressbar(self, orient="horizontal", length=80, mode="determinate")
        # self.progress.grid(row=1, column=0, pady=3, sticky='nesw')

    # def exec_button_loop(self):
    #     self.progress['maximum'] = 100
    #     for i in range(10):
    #         # update progressbar
    #         self.queue.put(self.progress.step())
    #         time.sleep(1)

    def start_thread(self, func):
        t = Thread(target=func)
        # close thread automatically after finishing task
        # t.setDaemon(True)
        print(self.show_threads())
        t.start()

    def show_threads(self):
        print(threading.active_count())

    def init_exec_button_loop(self):
        self.start_thread(self.exec_button_loop)

    def init_cmd_balance(self):
        self.start_thread(self.cmd_balance)

    def init_peers(self):
        self.start_thread(self.peers)

    def init_status(self):
        self.start_thread(self.status)

    def peers(self):
        self.console.input.delete(0, tk.END)
        epic_pass_api_v2 = 'DcxeGBwtZY3FlZcnDFmI'
        r = requests.get('http://localhost:23413/v1/peers/connected', auth=('epic', epic_pass_api_v2))
        users_info = ''
        for i in r.json()[0:5]:
            users_info = users_info + f"""
            User agent {str(i['user_agent'])} 
            Address {str(i['addr'])}
            At height: {str(i['height'])} ({str(i['direction'])})
            """
        peer_num = f"""
            Peers: {len(r.json())}, showing 5"""
        self.console.screen.insert(tk.END, "\n" + str(users_info))
        self.console.screen.yview(tk.END)

    def owner_api(self):
        password = "majkut11"
        cmds = f'epic-wallet -p {password} owner_api'.split(" ")
        proc = Popen(cmds, stdout=PIPE, stderr=PIPE, universal_newlines=True, bufsize=1)
        stdout, stderr = proc.communicate()
        print(stdout, stderr)

    def status(self):
        epic_pass_api_v2 = 'DcxeGBwtZY3FlZcnDFmI'
        r = requests.get('http://localhost:23413/v1/status', auth=('epic', epic_pass_api_v2))
        self.console.screen.insert(tk.END, "\n" + str(r.json()))
        self.console.screen.yview(tk.END)

    def cmd_balance(self):
        password = "majkut11"
        cmds = f'epic-wallet -p {password} info'.split(" ")
        proc = Popen(cmds, stdout=PIPE, stderr=PIPE, universal_newlines=True, bufsize=1)
        stdout, stderr = proc.communicate()
        print(stdout, stderr)
        self.console.screen.insert(tk.END, stdout + '\n' + stderr)
        self.console.screen.yview(tk.END)
        return proc


class WalletFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, **kwargs)
        self.args = args
        self.kwargs = kwargs
        resp_grid(self.master, 3, 1)
        self.grid()

        self.master.title('Epic-Cash CLI WALLET Wraper _alpha')

        self.header = HeaderFrame(self, bg='black', width=500, height=100, pady=3)
        self.body = BodyFrame(self, bg='yellow', padx=3, pady=3)
        self.footer = Frame(self, bg='white', pady=3)

        self.header.grid(row=0, column=0, sticky="nsew")
        self.body.grid(row=1, sticky="nsew")
        self.footer.grid(row=2, sticky="nsew")
