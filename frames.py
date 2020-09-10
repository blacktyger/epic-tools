import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import filedialog, Text
from PIL import Image, ImageTk
from tinydb import Query

from tools import *
from managers import *
from db import file_paths as db_paths


class Tab(ttk.Notebook):
    def __init__(self, master, **kwargs):
        ttk.Notebook.__init__(self, master, **kwargs)
        self.master = master


def show_list(master, list):
    for i, x in enumerate(list):
        get_db(db_paths)
        tk.Label(master, text=f"{x}").grid(column=0, row=i)


class FilesFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Manage widget grid (make it responsive, setup padding's)
        resp_grid(self, 1, 1, 10, 10)
        self.parent = parent
        self.command = None
        self.widget_names = ["Node", "Wallet", "API", "GPU Miner", "CPU Miner"]
        self.widget_objects = []
        self.entry = tk.Text(master=self.master.master.master.ctr_left, width=60)
        self.entry.grid(ipady=200)
        self.var = tk.StringVar()
        self.name_path = [
            {'name': name, 'path': os.path.split(path['entry'])[0], 'file': os.path.split(path['entry'])[1]}
            for name, path in zip(self.widget_names, db_paths.all())
            ]
        for i, widget in enumerate(self.name_path):
            if widget['name'] != "Wallet":
                pass
                # self.widget_objects.append(Button(
            #             widget=self, name=f"{widget['name']}", text=f"{widget['path']}",
            #             command=lambda widget=widget: do_cmdline(cmd=fr"START /min /D {widget['path']} {widget['file']}",
            #                                                      master=self.parent.parent.master.ctr_left,
            #                                                      entry=self.entry), grid=[i, 0]))
            else:
                bt = Button(
                    widget=self, name=f"{widget['name']}",
                    text=f"{widget['name']}",
                    command=threading.Thread(target=self.do_cmd).start, grid=[i, 0])
                self.widget_objects.append(bt)
                # self.entry.insert(tk.END, do_cmd)

            tk.Button(master=self, text=f"refresh db/ show list",
                      command=lambda: show_list(master=self.parent.parent.master.ctr_left,
                                                list=get_db(db_paths))).grid()

    def do_cmd(self):
        z = r""
        save = subprocess.run(fr"tree"
                              , capture_output=True, text=True)
        print(save.stderr)
        # print(save)
        self.entry.insert(tk.END, save.stdout + '\n' + save.stderr)
        print(save.stdout)


class PathsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Manage widget grid (make it responsive, setup padding's)
        resp_grid(self, 1, 1, 10, 10)
        self.parent = parent
        self.widget_names = ["Node", "Wallet", "API", "GPU Miner", "CPU Miner"]
        self.widget_objects = []

        for i, widget in enumerate(self.widget_names):
            self.widget_objects.append(ButtonEntry(
                widget=self, name=widget, grid=[i, 0]))
        self.check_db()
        self.btn_save = tk.Button(self, text=f"Save files paths", command=lambda: self.create_record())
        self.btn_save.grid(row=7)

        self.btn_show_db = tk.Button(self, text=f"SHOW DB", command=lambda: self.show_db())
        self.btn_show_db.grid(row=7, column=1)

    def check_db(self):
        if db_paths:
            for record in db_paths.all():
                for widget in self.widget_objects:
                    if record['name'] == widget.name:
                        widget.entry.delete(0, tk.END)
                        widget.entry.insert(0, record['entry'])
        else:
            pass

    def create_record(self):
        values_dict = {}
        for i, widget in enumerate(self.widget_objects):
            values_dict[widget.name] = widget.entry.get().replace('/', '\\')

        for i, (k, v) in enumerate(values_dict.items()):
            Widget = Query()
            db_paths.upsert({'name': k, 'entry': v}, Widget.name == k)

    def show_db(self):
        for k in db_paths.all():
            tk.Label(self.parent.parent.master.ctr_left, text=f"{k}").grid(columnspan=2)


class Header(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        resp_grid(self, 1, 1)
        Background(widget=self, img_path=r'C:\Users\IOPDG\Desktop\img\epiclogo.png')
        # Frames
        self.width_label = tk.Label(self, text=f'{get_frame_size(self)}')
        self.width_label.grid(row=1, column=0)


class Body(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        resp_grid(self, 1, 2, 30, 30)

        self.ctr_left = tk.Frame(self, bg='blue', width=400, height=300)
        self.ctr_right = tk.Frame(self, bg='green', width=250, height=300, padx=3, pady=3)

        self.ctr_left.grid(row=0, column=0, sticky=s['full'])
        self.ctr_right.grid(row=0, column=1, sticky=s['full'])

        self.nb = Tab(self.ctr_right)
        self.page0 = FilesFrame(self.nb, bg='green')
        self.page1 = PathsFrame(self.nb, bg='green')
        self.page2 = ttk.Frame(self.nb)

        self.nb.add(self.page0, text=f'Files')
        self.nb.add(self.page1, text=f'Files paths')
        self.nb.add(self.page2, text=f'Other')
        self.nb.grid(row=0, column=0, sticky=s['full'], ipady=10, ipadx=10)


class Footer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.width_label = tk.Label(self, text='Width:')
        self.entry_W = tk.Entry(self, background="pink")

        self.entry_W.grid(row=1, column=1)
        self.width_label.grid(row=1, column=0)
