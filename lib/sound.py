import subprocess

def play_mp3(file_path):
    subprocess.check_call(['mpg123', file_path])
