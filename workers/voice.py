import logging
from multiprocessing import Process, Queue
from threading import Thread
from time import sleep

from pocketsphinx import LiveSpeech

from utils.content import TextContent
from utils.infinite_worker import infinite_worker
from utils.sound import play_mp3


def get_workers(response, prefix):
    prefix = prefix.lower()

    queue = Queue()

    def input_worker(queue):
        speech = LiveSpeech(sampling_rate=16000,
                            lm='assets/dictionary/9126.lm',
                            dic='assets/dictionary/9126.dic',
                            audio_device='0')

        for phrase in speech:
            queue.put(phrase.hypothesis())

    def process_phrase_worker(phrase):
        def worker():
            logging.debug(u'Voice input: {}'.format(phrase))

            if not phrase.startswith(prefix):
                continue

            play_mp3('assets/speech-detected.mp3')

            if not response.maybe_handle(TextContent(body=phrase)):
                play_mp3('assets/error.mp3')

        return worker

    def processing_worker():
        while True:
            phrase = queue.get()
            if phrase is None or len(phrase) == 0:
                continue

            # Handling this phrase in a separate thread so we can keep keep processing the next one
            Thread(target=processing_worker(text.lower()), name='Phrase processing').start()

    return (Process(target=infinite_worker(input_worker), name='Voice input', args=[queue]),
        Thread(target=infinite_worker(processing_worker), name='Voice processing'))
