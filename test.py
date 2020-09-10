import subprocess
import sys
import tkinter as tk

# !/usr/bin/python
"""
- read output from a subprocess in a background thread
- show the output in the GUI
"""
import sys
from itertools import islice
from subprocess import Popen, PIPE
from textwrap import dedent
from threading import Thread

import tkinter as tk  # Python 3
from queue import Queue, Empty  # Python 3


def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return


class DisplaySubprocessOutputDemo:
    def __init__(self, root):
        self.root = root
        x = r"START /D C:\Users\IOPDG\Desktop\Mining stuff\epic-wallet epic-wallet.exe info"
        # start dummy subprocess to generate some output
        self.process = Popen(x, shell=True, stdout=PIPE)

        # launch thread to read the subprocess output
        #   (put the subprocess output into the queue in a background thread,
        #    get output from the queue in the GUI thread.
        #    Output chain: process.readline -> queue -> label)
        q = Queue(maxsize=1024)  # limit output buffering (may stall subprocess)
        t = Thread(target=self.reader_thread, args=[q])
        t.daemon = True  # close pipe if GUI process exits
        t.start()

        # show subprocess' stdout in GUI
        self.label = tk.Text(root, font=(None, 15))
        self.label.pack(ipadx=4, padx=4, ipady=4, pady=4, fill='both')
        self.update(q)  # start update loop

    def reader_thread(self, q):
        """Read subprocess output and put it into the queue."""
        try:
            with self.process.stdout as pipe:
                for line in iter(pipe.readline, b''):
                    q.put(line)
        finally:
            q.put(None)

    def update(self, q):
        """Update GUI with items from the queue."""
        for line in iter_except(q.get_nowait, Empty):  # display all content
            if line is None:
                # self.quit()
                return
            else:
                self.label.insert(tk.END, line)  # update GUI
                break  # display no more than one line per 40 milliseconds
        self.root.after(40, self.update, q)  # schedule next update

    def quit(self):
        self.process.kill()  # exit subprocess if GUI is closed (zombie!)
        self.root.destroy()


root = tk.Tk()
app = DisplaySubprocessOutputDemo(root)
root.protocol("WM_DELETE_WINDOW", app.quit)
# center window
# root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
root.mainloop()


# class TextBoxDemo(tk.Tk):
#     def __init__(self, parent):
#         tk.Tk.__init__(self, parent)
#         self.parent = parent
#         self.wm_title("TextBoxDemo")
#         self.textbox = tk.Text(self)
#         self.textbox.pack()
#
#         self.txt_var = tk.StringVar()
#         self.entry = tk.Entry(self, textvariable=self.txt_var)
#         self.entry.pack(anchor="w")
#
#         self.button = tk.Button(self, text="Add", command=self.add)
#         self.button.pack(anchor="e")
#
#     def add(self):
#         self.textbox.insert(tk.END, self.txt_var.get())
#
#
# if __name__ == '__main__':
#     try:
#         app = TextBoxDemo(None)
#         app.mainloop()
#     except _tk.TclError as e:
#         if platform.system() == 'Windows':
#             print(e)
#             print("Seems tk will not run; try running this program outside a virtualenv.")


# from tk import *
# from subprocess import Popen, PIPE, STDOUT, call, STARTUPINFO, STARTF_USESHOWWINDOW
#
# si = STARTUPINFO()
# si.dwFlags |= STARTF_USESHOWWINDOW
#
#
# def do_cmdline(cmd):
#     """Execute program in 'cmd' and pass 'text' to STDIN.
#     Returns STDOUT output.
#     Code from: https://stackoverflow.com/questions/8475290/how-do-i-write-to-a-python-subprocess-stdin
#     Note that any prompt the program writes is included in STDOUT.
#     """
#
#     process = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE, startupinfo=si)
#     result = process.communicate()[0].decode('utf-8')
#     return result.strip()
#
#
# def run_program(name, path):
#     try:
#         Popen(fr"START /min /D {path} {name}")
#     except KeyError as er:
#         print(er)
#
#
# class App:
#     def __init__(self, master):
#         frame = Frame(master)
#         frame.pack()
#
#         self.plain = Entry(frame, width=130)
#         self.plain.pack()
#
#         self.translate = Button(frame, text="ROT13", command=self.do_rot13)
#         self.translate.pack()
#
#         self.rot13 = Entry(frame, width=130)
#         self.rot13.pack()
#
#     def do_rot13(self):
#         # get the text we have to ROT13
#         plaintext = self.plain.get()
#         path = r"C:\Krypto\EPIC\epic_2.3.1-1"
#
#         # use the commandline program to do the translation
#         rot13text = do_cmdline(fr"START /min /D {path} {plaintext}")
#
#         # # strip off the prompt stuff
#         # (_, rot13text) = rot13text.split(': ')
#         #
#         # # update the ROT13 display
#         # self.rot13.delete(0, END)
#         self.rot13.insert(0, rot13text)
#         print(rot13text)
#
#
# root = Tk()
# app = App(root)
# root.mainloop()
