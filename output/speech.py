import os
import subprocess
from gtts import gTTS

from output import Output


class Speech(Output):

    def __init__(self, pre_speech=None):
        super(Speech, self).__init__()
        self.pre_speech = pre_speech

    def output(self, string):
        if self.pre_speech is not None:
            self.pre_speech()

        file_path='speech.mp3'

        try:
            os.remove(file_path)
        except OSError:
            pass # file doesn't exist, no need to freak out

        tts = gTTS(text=string, lang='en')
        tts.save(file_path)

        subprocess.check_call(['mpg123', '--delay', '2', file_path])

        os.remove(file_path)
