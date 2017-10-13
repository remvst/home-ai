import os
import threading
from time import sleep

import config
from utils.sound import play_mp3, text_to_speech, pair_speaker


queue = []
lock = threading.Lock()

def add_to_queue(string):
    lock.acquire()
    queue.append(string)
    lock.release()

def worker():
    while True:
        lock.acquire()

        try:
            # Play first item in the queue
            if len(queue) > 0:
                play_string(queue.pop(0))
        finally:
            lock.release()

        sleep(0.5)

def play_string(string):
    file_path = 'speech.mp3'

    try:
        os.remove(file_path)
    except OSError:
        pass # file doesn't exist, no need to freak out

    text_to_speech(string=string, file_path=file_path)
    pair_speaker(mac_address=config.SPEAKER_MAC_ADDRESS, sink_name=config.SINK_NAME)

    play_mp3('speech-announcement.mp3')
    play_mp3(file_path)

    os.remove(file_path)
