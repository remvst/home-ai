import logging

from pocketsphinx import LiveSpeech

from utils.content import TextContent
from utils.sound import play_mp3

def get_worker(response, prefix):
    speech = LiveSpeech(sampling_rate=16000,
                        lm='assets/dictionary/9126.lm',
                        dic='assets/dictionary/9126.dic',
                        audio_device='0')

    prefix = prefix.lower()

    def worker():
        for phrase in speech:
            text = phrase.hypothesis().lower()
            logging.debug('Text to speech: {}'.format(text))

            if not text.startswith(prefix):
                continue

            play_mp3('assets/speech-detected.mp3')

            if not response.maybe_handle(TextContent(body=text)):
                play_mp3('assets/error.mp3')

    return worker
