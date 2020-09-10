import tkinter as tk
from datetime import datetime
from tkinter import filedialog, Text
import os
from distutils.dir_util import copy_tree
from check_process import Program, Command, process_manager, check_process


def backup():
    source = filedialog.askdirectory(
        initialdir="C:\Krypto\EPIC", title="Directory to backup")
    source = os.path.normpath(source)
    destination = filedialog.askdirectory(
        initialdir=source, title="Destination for backup")
    destination = os.path.normpath(destination)
    folder_name = source.split(os.sep)[-1]
    backup_folder = f"{folder_name}_{datetime.today().strftime('%Y-%m-%d_%H;%M')}"
    copy_tree(source, os.path.join(destination, backup_folder))
    print(f"BACKUP from: {source} to: {destination}\\{backup_folder} completed")
    return True


# programs = [
#     Program(name='node', process_name='epic.exe', path=r'C:\Krypto\EPIC\epic_2.3.1-1'),
#     Program(name='cpu_miner', process_name='epic-miner.exe', path=r'C:\Krypto\EPIC\epic-miner_2.3.1-1'),
#     Program(name='gpu_miner', process_name='epic-miner.exe', path=r'C:\Krypto\EPIC\epic-miner-opencl_2.3.1-1'),
#     ]

# commands = [
#     Command(name='wallet_listener', process_name='epic-wallet-listen.bat',
#             path=r'C:\Krypto\EPIC\epic-wallet', exe_file='epic-wallet.exe'),
#     ]


# def run_program(name, path):
#     try:
#         os.system(fr"START /D {path} {name}")
#     except KeyError as er:
#         print(er)
#
#
# def run_all():
#     for p in programs:
#         run_program(p.process_name, p.path)
#     for c in commands:
#         run_program(c.process_name, c.path)
#
#
# def check_process():
#     for p in programs:
#         print(process_manager(p.process_name, get_list=True))
#
#
# def kill():
#     for p in programs:
#         process_manager(p.process_name, kill=True)
#     for c in commands:
#         cmds = process_manager(c.exe_file, get_list=True)
#         print(cmds)
#         for cmd in cmds:
#             for x in cmd.children(recursive=True):
#                 x.kill()
#             cmd.kill()
#     process_manager('cmd.exe', kill=True)

files_list = []

if os.path.isfile('files.txt'):
    with open('files.txt', 'r') as f:
        temp_files = f.read()
        temp_files = temp_files.split(',')
        files_list = [file for file in temp_files if file.strip()]


def add_file(frame):
    for widget in body.winfo_children():
        widget.destroy()

    file_name = filedialog.askopenfilename(
        initialdir=r"C:\Users\IOPDG\Desktop\Mining stuff", title="Select path",
        filetypes=(("exec files", "*.exe"), ("bat files", "*.bat")))

    # if file_name not in files_list:
    #     files_list.append(file_name)
    # for file in files_list:
    label = tk.Label(frame, text=file_name)
    label.pack(side=tk.LEFT)


def run_files():
    for file in files_list:
        file_name = str(file.split("/")[-1])
        print(file_name)
        if not check_process(file_name):
            os.startfile(file)
        else:
            print(f"{file_name} already running")


root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=700, bg='gray90', relief='raised')
canvas.pack()

header = tk.Frame(root, bg='black')
header.place(relwidth=1, relheight=0.1)

server = tk.Frame(root, bg='#E6B62C')
server.place(relwidth=0.8, relheight=0.2, relx=0.1, rely=0.1)

body = tk.Frame(root, bg='white')
body.place(relwidth=0.8, relheight=0.4, relx=0.1, rely=0.5)

buttons = tk.Frame(root, bg="red")
buttons.place(relwidth=0.6, relheight=0.3, relx=0.2, rely=0.8)

select_files = tk.Button(server, text="Server path", padx=10, pady=5,
                         fg='red', bg='black', command=lambda: add_file(server))
run = tk.Button(buttons, text="Run all files", padx=20, pady=10,
                fg='white', bg='blue', command=run_files)
backup = tk.Button(body, text="Backup chain data", padx=20, pady=10,
                   fg='white', bg='#17BBAF', command=backup)
run.pack()
backup.pack()

title = tk.Label(header, text="Epic miners toolkit")
server_title = tk.Label(server, text="Epic-Cash Server", bg='#E6B62C')

server_title.pack()
select_files.pack(side=tk.LEFT)

title.pack()

for file in files_list:
    label = tk.Label(body, text=file)
    label.pack()

root.mainloop()

with open('files.txt', 'w') as f:
    for file in files_list:
        f.write(file + ',')
