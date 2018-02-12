import logging

logging.debug('Initializing speech things maybe')

from pocketsphinx import LiveSpeech

from bot.kik_bot import bot
from workers.speech import add_to_queue

logging.debug('Initializing speech things')
speech = LiveSpeech(sampling_rate=16000, lm='assets/dictionary/9126.lm', dic='assets/dictionary/9126.dic', audio_device='0')
logging.debug('Initialized speech things')

def worker():
    for phrase in speech:
        text = phrase.hypothesis()
        logging.debug('GOOOOOOOOOOO')
        logging.debug(text)

        if 'please' not in text:
            continue

        if not bot.handle_text(text):
            add_to_queue('unrecognized command')
