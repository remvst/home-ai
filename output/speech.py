import os
import subprocess
from gtts import gTTS

from output import Output


class Speech(Output):

    def output(self, string):
        file_path='speech.mp3'

        try:
            os.remove(file_path)
        except OSError:
            pass # file doesn't exist, no need to freak out

        tts = gTTS(text=string, lang='en')
        tts.save(file_path)

        subprocess.check_call(['mpg123', '--delay', '2', file_path])

        os.remove(file_path)
