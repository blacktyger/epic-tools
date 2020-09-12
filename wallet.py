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
from decimal import *
from PIL import Image, ImageTk
from tinydb import Query

from server import Server
from tools import *
from managers import *
import db
import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.threaded import pool

getcontext().prec = 8


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


class Command(Thread):
    def __init__(self, command, password, node="local_node"):
        self.command = command
        self.password = password
        if node == "local_node":
            self.full_cmd = f'epic-wallet -p {self.password} {command}'.split(" ")
        else:
            self.full_cmd = f'epic-wallet -p {self.password} -r {node} {command}'.split(" ")
        Thread.__init__(self)

        process = Popen(self.full_cmd, stdout=PIPE, stderr=PIPE,
                        universal_newlines=True, bufsize=1)
        self.stdout, self.stderr = process.communicate()
        # print(self.stdout)


class WalletInterface(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        print('gui')
        self.balance = tk.StringVar()
        self.bg_img = tk.PhotoImage(file=r'C:\epic-tools\img\main_screen_bg.png')
        self.btns_area = tk.Canvas(self, width=450, height=800, borderwidth=0,
                                   highlightthickness=0)
        self.balance = tk.StringVar()

        self.columnconfigure(0, minsize=500, weight=1)
        self.grid_rowconfigure(0, minsize=750, weight=1)

        # WalletInterface Widgets
        self.btns_area.grid(sticky="news")
        self.btns_area.create_image(0, 0, image=self.bg_img, anchor='nw')
        self.get_balance()
        self.btns_area.create_text(240, 105, fill="gold", font="Times 28 bold",
                                   text=self.balance.get())
        
        self.run_console_btn = tk.Button(self, text="Run command line console",
                                         command=self.master.wallet.run_console, **kwargs)
        self.btns_area.create_window(int(self.btns_area['width']) / 2, 600,
                                     window=self.run_console_btn)

    def get_balance(self):
        data = APIManager()
        balance = data.run_query(query="retrieve_summary_info")
        self.balance.set(balance)


class APIManager:
    def __init__(self, api_secret="DcxeGBwtZY3FlZcnDFmI", url=fr"http://localhost:23420/v1/wallet/owner/"):
        self.url = url
        self.api_secret = api_secret
        self.auth = ('epic', self.api_secret)

    def run_query(self, query, params="", output='json'):
        response = {}
        r = requests.get(self.url + query + params, auth=self.auth)
        print(self.url + query + params)
        if output == 'json':
            response = r.json()[1]
            data = Decimal(response['total']) / 10 ** 8
            data = data.quantize(Decimal('.0001'), rounding=ROUND_UP)
            return data

    def insert(self, widget, query):
        data = Decimal(self.run_query(query=query)['total']) / 10 ** 8
        data = data.quantize(Decimal('.0001'), rounding=ROUND_UP)
        widget.insert(tk.END, data)

    def match_query(self):
        pass


class Wallet:
    def __init__(self, master, login_redirect=None):
        self.master = master
        self.accounts = ['default']
        self.password = tk.StringVar()
        self.db = db
        self.button_clicked = False
        self.login_redirect = login_redirect
        # self.server = Server(master=self.master)
        self.online_nodes = ["http://95.216.215.107:3413/"]
        self.node = self.online_nodes[0]

    def run_console(self):
        new_window = tk.Toplevel(self.master)
        self.wallet_window = WalletFrame(new_window)
        self.wallet_window.master.geometry('770x600+630+0')
        resp_grid(self.wallet_window, 2, 2)
        self.wallet_window.grid(sticky="nswe")

    def password_input(self, widget, **kwargs):
        self.input = tk.Entry(master=widget, bg="#52504a",
                              show="*", **kwargs)
        self.input.bind('<Return>', self.login)
        return self.input

    def send_password_btn(self, widget, **kwargs):
        self.widget = widget
        self.button = tk.Button(master=widget, text="Login to wallet",
                                command=self.login, **kwargs)
        self.button.bind('<Return>', self.login)
        return self.button

    def login(self, event=None):
        self.password = self.input.get()
        self.input.delete(0, tk.END)
        print(f"{self.password} saved")
        self.widget.itemconfigure(self.master.pass_info, text="Loading...")

        if self.check_password():
            self.widget.delete('all')
            self.widget.destroy()
            self.interface = WalletInterface(master=self.master)
            self.interface.grid(sticky="news")

        else:
            self.widget.itemconfigure(self.master.pass_info, text="Wrong password")
            print("NIE")
            pass

    def check_password(self):
        check = Command(command="info", password=self.password, node=self.node)
        check.start()
        check.join()

        invalid = "Invalid Arguments: Error decrypting wallet seed (check provided password)"
        success = "Command 'info' completed successfully"
        if invalid in (check.stdout):
            print('pass invalid')
            return False
        if success in (check.stdout):
            print('pass valid!!')
            return True

    def server_is_online(self):
        check = Command(command="info", password="majkut11", node=self.node)
        check.start()
        check.join()
        offline = "WARNING: Wallet failed to verify data against a live"
        if offline in check.stdout:
            print("OFFLINE")
            return False
        else:
            print("ONLINE")
            return True

    def get_seed_file(self):
        print("Clicked!")
        if len(db.file_paths.search(Query()['name'] == "seed")) == 0:
            file_name = filedialog.askopenfilename(
                initialdir=r"C:", title="Select path",
                filetypes=(("all files", "*.*"), ("wallet seed file", "*.seed")))
            self.db.file_paths.insert({'name': 'seed', 'entry': file_name})
            print(f"{file_name} added to db")
            # copy2(file_name, os.getcwd())
            # return db.file_paths.get(Query()['name'] == "seed")['entry']

    def seed_phrase(self):
        pass

    def get_secret_api(self):
        pass

    def thread_command(self, target):
        t = Thread(target=target)
        t.run()

    def command(self, command):
        cmd = f'epic-wallet -p {self.password} {command}'.split(" ")
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True, bufsize=1)
        stdout, stderr = process.communicate()
        print(stdout, stderr)
        # self.console.screen.insert(tk.END, stdout + '\n' + stderr)
        # self.console.screen.yview(tk.END)
        return process

    # def encrypt_password(self):
    #


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
