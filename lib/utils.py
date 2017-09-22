import os
import subprocess
from gtts import gTTS

def is_user_in_network(mac_address, timeout=5000):
    arp_scan = subprocess.check_output([
        'arp-scan',
        '-l',
        '--timeout={}'.format(timeout)
    ])
    return mac_address in arp_scan

def say(text):
    file_path='speech.mp3'

    try:
        os.remove(file_path)
    except OSError:
        pass # file doesn't exist, no need to freak out

    tts = gTTS(text=text, lang='en')
    tts.save(file_path)

    subprocess.check_call(['mpg123', file_path])

    os.remove(file_path)
