import logging

from pocketsphinx import LiveSpeech

from bot.kik_bot import bot
from workers.speech import add_to_queue

speech = LiveSpeech(sampling_rate=16000, lm='assets/dictionary/9126.lm', dic='assets/dictionary/9126.dic', audio_device='0')

def worker():
    for phrase in speech:
        text = phrase.hypothesis().lower()
        logging.debug('Text to speech: {}'.format(text))

        if not text.startswith('please'):
            continue

        if not bot.handle_text(text):
            add_to_queue('unrecognized command')
