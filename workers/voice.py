import logging
from multiprocessing import Process, Queue
from threading import Thread

from pocketsphinx import LiveSpeech

from utils.content import TextContent
from utils.infinite_worker import infinite_worker
from utils.sound import play_mp3_threaded


class VoiceProcessor(object):

    def __init__(self, prefix, response):
        super(VoiceProcessor, self).__init__()

        self.prefix = prefix.lower()
        self.response = response

        self.queue = Queue()
        self.paused = False

    def pause_processing(self):
        logging.debug('pause processing')
        self.paused = True

    def resume_processing(self):
        logging.debug('resume processing')
        self.paused = False

    def input_worker(self):
        def worker(queue):
            speech = LiveSpeech(sampling_rate=16000,
                                lm='assets/dictionary/3306.lm',
                                dic='assets/dictionary/3306.dic',
                                audio_device='0')

            for phrase in speech:
                logging.debug('Voice input: {}, probability: {}'.format(phrase.hypothesis(), phrase.probability()))
                queue.put(phrase.hypothesis())

        process = Process(target=infinite_worker(worker), name='Voice input', args=[self.queue])
        process.daemon = True  # make sure this process dies at the same time as the current one
        return process

    def processing_worker(self):
        def worker():
            while True:
                logging.debug('wait for queue...')
                phrase = self.queue.get()
                logging.debug('got queue element')

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

            input_content = TextContent(body=phrase)

            # Play a sound before we even handle the input
            if self.response.should_handle(input_content):
                play_mp3_threaded('assets/speech-detected.mp3')
            else:
                play_mp3_threaded('assets/error.mp3')

            # Actually handle the input
            self.response.maybe_handle(input_content)

        return Thread(target=worker, name='Phrase processing')
