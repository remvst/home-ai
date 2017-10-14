import os
import threading
from time import sleep
from uuid import uuid4

import config
from utils.sound import play_mp3, text_to_speech, pair_speaker


queue = []
lock = threading.Lock()

def add_to_queue(string):
    file_path = 'static/speech/{}.mp3'.format(str(uuid4))
    text_to_speech(string=string, file_path=file_path)

    profile_cascade = cv2.CascadeClassifier('assets/haarcascade_profileface.xml')

    lock.acquire()
    queue.append(file_path)
    lock.release()

def worker():
    while True:
        lock.acquire()

        try:
            # Play first item in the queue
            if len(queue) > 0:
                play_speech(queue.pop(0))
        finally:
            lock.release()

        sleep(0.5)

def play_speech(file_path):
    pair_speaker(mac_address=config.SPEAKER_MAC_ADDRESS, sink_name=config.SINK_NAME)

    play_mp3('assets/speech-announcement.mp3')
    play_mp3(file_path)

    os.remove(file_path)
