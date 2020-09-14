import psutil
import time
from datetime import datetime

now = datetime.now().strftime('%H:%M:%S')


class Program:
    def __init__(self, name, process_name, path):
        self.name = name
        self.process_name = process_name
        self.path = path
        self.cmd_name = process_name

    def __str__(self):
        return f"{self.name}"


class Command(Program):
    def __init__(self, name, process_name, path, exe_file, cmd='cmd.exe'):
        super().__init__(name, process_name, path)
        self.exe_file = exe_file
        self.cmd = cmd

    def __str__(self):
        return f"CMD: {self.name}, file: {self.exe_file}"


def check_process(name):
    # Iterate over the all the running process
    for process in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if name.lower() in process.name().lower():
                return process
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def get_process_id(name):
    process_list = []
    # Iterate over the all the running process
    for process in psutil.process_iter():
        try:
            pinfo = process.as_dict(attrs=['pid', 'name', 'create_time'])
            # Check if process name contains the given name string.
            if name.lower() in pinfo['name'].lower():
                process_list.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_list


def kill_process(process):
    try:
        process.kill()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as er:
        print(er)
        pass
    return print(f"[{now}]: (PID:{process.ppid()}) {process.name()} is closed")


def process_manager(name, kill=False, get_list=False):
    # Check if process :name was running or not.
    try:
        if check_process(name):
            # Find details of all the running instances of process that contains :name
            process_list = [proc for proc in psutil.process_iter() if name in proc.name().lower()]
            if len(process_list) > 0:
                for process in process_list:
                    # print(f"[{now}]: {str(process).split('(')[1][:-1]}")
                    if kill:
                        kill_process(process)
                        print(f"{process} killed")
            else:
                return False

            if get_list:
                return process_list
        else:
            print(f'No {name} process was running')
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as err:
        print(err)
        pass
