import subprocess
from threading import Thread

from gtts import gTTS


def pair_speaker(mac_address, sink_name):
    subprocess.check_call(['./sh/pair_speaker', mac_address, sink_name])


def play_mp3(file_path, delay=0):
    subprocess.check_output(['mpg123', '--quiet', '--delay', str(delay), file_path])


def play_mp3_threaded(file_path, delay=0):

    def worker():
        play_mp3(file_path, delay)

    thread = Thread(target=worker)
    thread.daemon = True
    thread.start()


def text_to_speech(string, file_path='speech.mp3'):
    tts = gTTS(text=string, lang='en')
    tts.save(file_path)
