import os
import psutil
import sys

def restart_process():
    p = psutil.Process(os.getpid())
    for handler in p.get_open_files() + p.connections():
        os.close(handler.fd)

    python = sys.executable
    os.execl(python, python, *sys.argv)
