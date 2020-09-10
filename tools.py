import threading
import time
import queue
from datetime import datetime
from subprocess import Popen, PIPE, STARTUPINFO, STARTF_USESHOWWINDOW
from threading import current_thread
from tkinter import ttk
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, Text

import requests
from PIL import Image, ImageTk

si = STARTUPINFO()
# si.dwFlags |= STARTF_USESHOWWINDOW
s = {
    'full': 'wens',
    'x': 'we',
    'y': 'ns'
    }


class Robot(threading.Thread):
    def __init__(self, name, label_queue, func):
        super().__init__(name=name)
        self.daemon = True
        self.label_queue = label_queue
        self.func = func

    def run(self):
        while True:
            q = self.func()
            self.label_queue.put(q)
            time.sleep(1)


class LabelUpdater(threading.Thread):
    def __init__(self, master, name, label_queue, variable):
        super().__init__(name=name)
        self.daemon = True
        self.label_queue = label_queue
        self.master = master
        self.variable = variable

    def run(self) -> None:
        # run forever
        while True:
            # wait a second please
            time.sleep(1)
            # consume all the queue and keep only the last message
            last_msg = None
            while True:
                try:
                    msg = self.label_queue.get(block=False)
                except queue.Empty:
                    break
                last_msg = msg
                self.label_queue.task_done()
            if last_msg:
                self.variable.set(last_msg)


class NodeStatus(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.label_queue = queue.Queue()
        self.text = tk.StringVar()
        self.text.set(" Connecting to node...")
        self.label = tk.Label(self, textvariable=self.text).grid()
        self.robot = Robot("robot", self.label_queue, self.node_status)
        self.updater = LabelUpdater(master=self, name="updater",
                                    label_queue=self.label_queue,
                                    variable=self.text)
        self.updater.start()
        self.robot.start()

    def node_status(self):
        epic_pass_api_v2 = 'DcxeGBwtZY3FlZcnDFmI'
        try:
            r = requests.get('http://localhost:23413/v1/status', auth=('epic', epic_pass_api_v2))
            q = f"Block: {str(r.json()['tip']['height'])}   Peers: {str(r.json()['connections'])  }"
            self.text.set(q)
        except requests.exceptions.ConnectionError as e:
            self.text.set(f" Connecting to node...")


def get_db(db):
    return db


def get_color(status):
    if status == "Online":
        return "green"
    else:
        return "red"


def get_frame_size(widget):
    widget.update()
    return widget.grid_size()


def do_cmdline(cmd, extra=""):
    """Execute program in 'cmd' and pass 'text' to STDIN.
    Returns STDOUT output.
    Note that any prompt the program writes is included in STDOUT.
    """

    process = Popen(f"{cmd} {extra}", shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE, startupinfo=si)
    result = process.communicate()[0].decode('utf-8')
    return result.strip()


def resp_grid(parent, rows, columns, r_minsize=0, c_minsize=0):
    for i in range(rows):
        parent.grid_rowconfigure(i, minsize=r_minsize, weight=1)
    for i in range(columns):
        parent.grid_columnconfigure(i, minsize=c_minsize, weight=1)


def workers(number):
    with open('workers', 'w', encoding='utf-8') as f:
        f.write(number)


def save_to_file(data, file):
    # data = data.decode('utf-8')
    # json_data = json.loads(data)
    for line in str(data).split("b'"):
        line = line.replace("\\n'", "")
        with open(file, 'a', encoding='utf-8') as f:
            f.write(str(current_thread()))
            f.write(str(Msg(line)))
            f.write('\n')

        # for line in str(data).split("'"):
        #     print(line)
        # for x in line: # split('{'):
        #     print(x)


class Msg:
    def __init__(self, text, title='info'):
        self.title = str(title)
        self.text = str(text)

    def get_title(self):
        titles = {"-- @ INFO --": ['info', 'i', '@'],
                  "-- * WARN  --": ['warn', '*', 'w'],
                  "-- ! ERROR --": ['error', '!', 'e']}
        for string, sign in titles.items():
            # print(sign, string)
            if self.title in sign:
                return string

    def show(self):
        print(f'{self.get_title()} [{datetime.now().strftime("%H:%M:%S")}]: {str(current_thread()).split("(")[1].replace(")", "").split(" ")[0]} {self.text}')

    def __repr__(self):
        return f'{self.get_title()}[{datetime.now().strftime("%H:%M:%S")}]: {self.text}'

