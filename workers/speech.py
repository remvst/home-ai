import logging
import os
import threading
from uuid import uuid4

from utils.content import TextContent
from utils.output import Output
from utils.sound import play_mp3, text_to_speech, pair_speaker


class SpeechOutput(Output):

    def __init__(self, speaker_mac_address, sink_name, *args, **kwargs):
        super(SpeechOutput, self).__init__(*args, **kwargs)
        self.speaker_mac_address = speaker_mac_address
        self.sink_name = sink_name

        self.queue = []
        self.lock = threading.Lock()

    def output(self, contents):
        string = '.'.join([c.body for c in contents if isinstance(c, TextContent)])

        logging.debug(u'Adding to queue: {}'.format(string))

        file_path = 'static/speech/{}.mp3'.format(str(uuid4()))
        text_to_speech(string=string, file_path=file_path)

        logging.debug('Done with text_to_speech')

        self.lock.acquire()
        self.queue.append(file_path)
        self.lock.release()

        logging.debug('Added to queue')

    def get_worker(self):
        def worker():
            while True:
                self.lock.acquire()

                try:
                    # Play first item in the queue
                    if len(self.queue) > 0:
                        self._play_speech(self.queue.pop(0))
                finally:
                    self.lock.release()

        return worker

    def _play_speech(self, file_path):
        pair_speaker(mac_address=self.speaker_mac_address,
                     sink_name=self.sink_name)

        play_mp3('assets/speech-announcement.mp3')
        play_mp3(file_path)

        os.remove(file_path)
