import os
import psutil
import sys

def restart_process():
    python = sys.executable
    os.execl(python, python, *sys.argv)
