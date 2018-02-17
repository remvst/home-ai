import logging
from multiprocessing import Process, Queue
from threading import Thread

from pocketsphinx import LiveSpeech

from utils.content import TextContent
from utils.infinite_worker import infinite_worker
from utils.sound import play_mp3


class VoiceProcessor(object):

    def __init__(self, prefix, response):
        super(VoiceProcessor, self).__init__()

        self.prefix = prefix.lower()
        self.response = response

        self.queue = Queue()
        self.paused = False

    def pause_processing(self):
        self.paused = True

    def resume_processing(self):
        self.paused = False

    def input_worker(self):
        def worker(queue):
            speech = LiveSpeech(sampling_rate=16000,
                                lm='assets/dictionary/3306.lm',
                                dic='assets/dictionary/3306.dic',
                                audio_device='0')

            for phrase in speech:
                queue.put(phrase.hypothesis())

        return Process(target=infinite_worker(worker), name='Voice input', args=[self.queue])

    def processing_worker(self):
        def worker():
            while True:
                phrase = self.queue.get()

                if self.paused:
                    continue

                if phrase is None or len(phrase) == 0:
                    continue

                # Handling this phrase in a separate thread so we can keep keep processing the next one
                self._process_phrase_worker(phrase.lower()).start()

        return Thread(target=infinite_worker(worker), name='Voice processing')

    def _process_phrase_worker(self, phrase):
        phrase = phrase.lower()

        def worker():
            logging.debug(u'Voice input: {}'.format(phrase))

            if not phrase.startswith(self.prefix):
                return

            play_mp3('assets/speech-detected.mp3')

            if not self.response.maybe_handle(TextContent(body=phrase)):
                play_mp3('assets/error.mp3')

        return Thread(target=worker, name='Phrase processing')
