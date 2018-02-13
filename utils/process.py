import os
import sys

def restart_process():
    python = sys.executable
    os.execl(python, python, *sys.argv)
