import subprocess

def play_mp3(file_path):
    subprocess.check_output(['mpg123', file_path, '--quiet'])
