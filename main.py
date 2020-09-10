import json
import socket
import sys
import traceback
from ast import literal_eval
from threading import Thread, get_ident, current_thread, active_count
import logging

from thread import thread
from tools import Msg, save_to_file

"""
- Connect socket between miner and node
- fetch data from both and send back and forth
- one miner = one thread
- numbers of threads = numbers of miner workers (find number of active threads)

- create telegram bot
- create model for each user
- get data from users and save in db:
    * IPs and ports node <-> miner
    * 
- create commands and alerts for users about worker numbers

"""


def start_server():
    host = "localhost"
    port = 3416  # port for miners
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    Msg(f"Socket created")
    try:
        soc.bind((host, port))
    except:
        Msg("Bind failed. Error : " + str(sys.exc_info()), 'e')
        sys.exit()
    soc.listen()  # queue up to .... requests
    Msg(f"Server start listening {host}:{port} for miners")
    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        Msg(f"Connected with {ip}:{port}")
        try:
            Msg("THREAD: Start")
            Thread(target=thread, args=(connection, ip, port, host)).start()
        except:
            Msg("Thread did not start. Huston we have problem", 'e')
            # traceback.print_exc()


def main():
    start_server()


if __name__ == "__main__":
    main()
