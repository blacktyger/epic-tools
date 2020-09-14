import queue
import subprocess
import tkinter as tk
import os
from threading import Thread
from time import sleep
from tkinter import filedialog

import requests
from tinydb import Query

from check_process import check_process, process_manager
from db import file_paths as db_paths
from managers import Background
from tools import NodeStatus, Robot, LabelUpdater, get_color


class Server:
    def __init__(self, master):
        self.master = master
        self.sync = NodeStatus(self.master)
        self.status = tk.StringVar()
        self.status.set(self.check_status())
        self.button = self.button()

    def button(self, **kwargs):
        if self.status.get() == "Online":
            return tk.Button(self.master, text=f"Close Server",
                             command=self.quit_server, fg="red",
                             **kwargs)
        else:
            return tk.Button(self.master, text=f"Run Server",
                             command=self.run_server, fg="green",
                             **kwargs)

    def check_path(self):
        if db_paths.get(Query().name == "Node"):
            print(f"Node path exists")
            return db_paths.get(Query().name == "Node")['entry']
        else:
            print(f"NO NODE PATH")
            return False

    def set_path(self):
        file_name = filedialog.askopenfilename(
            initialdir=r"C:\Users\IOPDG\Desktop\Mining stuff", title="Select path",
            filetypes=(("exec files", "*.exe"), ("bat files", "*.bat")))
        db_paths.insert({'name': 'Node', 'entry': file_name})
        self.run_server()

    def check_status(self):
        if self.check_path():
            file_name = os.path.split(self.check_path())[1]
            if not check_process(file_name):
                return f"Offline"
            else:
                print("exp_height: ", self.sync.explorer_height.get())
                print("node_height: ", self.sync.node_height.get())
                return f"Online"
        else:
            return f"Offline"

    def run_server(self):
        def config():
            self.button.config(text='Close Server', command=self.quit_server,
                               fg="red")
            self.status.set("Sync...")
            print(f"changed to {self.status.get()}")

            self.sync.text.set("Sync...")
            self.master.change_color()

            print(self.sync.explorer_height.get())
            print(self.sync.node_height.get())

            self.status.set("Online")
            self.master.change_color()
            print(f"changed to {self.status.get()}")

        if self.check_path():
            # self.entry.insert(tk.END, save.stdout + '\n' + save.stderr)
            file_name = os.path.split(self.check_path())[1]
            file_path = os.path.split(self.check_path())[0].replace('/', '\\')
            if not check_process(file_name):
                self.process = subprocess.run(fr"START /min /D {file_path} {file_name}",
                                              capture_output=True, text=True, shell=True)
                print(self.process.stderr)
                print(self.process.stdout)
                config()
            else:
                print(f"{file_name} already running")
                config()
        else:
            self.set_path()

    def quit_server(self):
        file_name = os.path.split(self.check_path())[1]
        if check_process(file_name):
            process_manager(file_name, kill=True)
            self.status.set("Offline")
            self.master.change_color()
            print(f"changed to {self.status.get().lower()}")
            self.button.config(text="Run Server", command=self.run_server,
                               fg="green")
