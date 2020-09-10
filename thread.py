import socket
from threading import active_count

from tools import Msg, save_to_file, workers


def thread(connection, ip, port, host):
    Msg(f"{ip}:{port} ({host}) running...").show()
    host = "localhost"
    port = 23416
    is_active = True
    to_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    to_server_socket.connect((host, port))
    Msg(f"Connect to {host}:{port} || Active threads:{active_count()}").show()

    while is_active:
        try:
            miner_data = connection.recv(4024)
            save_to_file(miner_data, 'miner-server.txt')
            Msg(f"miner_data created").show()
            to_server_socket.send(miner_data)
            Msg(f"miner_data send to_server_socket").show()

            server_data = to_server_socket.recv(4024)
            save_to_file(server_data, 'server_miner.txt')
            Msg(f"server_data created").show()
            connection.send(server_data)
            Msg(f"server_data send miner").show()

        except ConnectionResetError:
            break
        workers(str(active_count()))



"""
Hey Keith!

I'm Patryk, good friend of Szymon :). He told me that you are looking for help with 
maintaining your website and editing YouTube videos, is that right? 
If yes, I would love to hear some more in details and see if I'm able to help you :)

Something about me:

Born in Poland, living in Scotland for past 5 years, full time joiner and dad, geek from heart :)
More than a year a go I decided to change my hobby to my job and became a web developer - since that day
I spend every second of my free time mastering those things. 

https://epic-ticker.tech/ - that's my current project I'm working on my own - everything made from scratch - 
I heard you are also DIY with your site and YouTube and I need to admit it's looking awesome :) Great work!
My project is doing various market analysis of Epic-Cash cryptocurrency (like Bitcoin), 
so design is simple to serve users easy to read content, and most work is done 'behind the scenes' :). 

I'm learning at this moment all kinds of stuff related to this things, 
I've done some projects on WordPress years ago, but I'm still up to date with 
this framework and tools like elementor. 

I hope to hear from you, and have a nice Sunday! (as you certainly know, in Scotland it's raining now...)

"""

