import subprocess

from gtts import gTTS


def pair_speaker(mac_address, sink_name):
    subprocess.check_call(['./sh/pair_speaker', mac_address, sink_name])


def play_mp3(file_path, delay=0):
    subprocess.check_output(['mpg123', '--quiet', '--delay', str(delay), file_path])


def text_to_speech(string, file_path='speech.mp3'):
    tts = gTTS(text=string, lang='en')
    tts.save(file_path)
