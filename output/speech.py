import os
import threading
from gtts import gTTS
from uuid import uuid4

from lib.sound import play_mp3
from output import Output


class Speech(Output):

    def __init__(self, pre_speech=None):
        super(Speech, self).__init__()
        self.pre_speech = pre_speech
        self.queue = []

        self.lock = threading.Lock()

    def output(self, string):
        self.lock.acquire()
        self.queue.append(string)
        self.lock.release()

    def playback_worker(self):
        while True:
            self.lock.acquire()

            if len(self.queue) > 0:
                # Play first item in the list
                self.play_string(self.queue.pop(0))

            self.lock.release()

    def play_string(self, string):
        file_path = '/tmp/speech.mp3'

        try:
            os.remove(file_path)
        except OSError:
            pass # file doesn't exist, no need to freak out

        tts = gTTS(text=string, lang='en')
        tts.save(file_path)

        if self.pre_speech is not None:
            self.pre_speech()

        play_mp3(file_path)

        os.remove(file_path)
