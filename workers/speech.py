import logging
import os
from threading import Thread
from uuid import uuid4

from utils.content import TextContent
from utils.infinite_worker import infinite_worker
from utils.output import Output
from utils.sound import play_mp3, text_to_speech, pair_speaker


class SpeechOutput(Output):

    def __init__(self, speaker_mac_address, sink_name):
        super(SpeechOutput, self).__init__()

        self.speaker_mac_address = speaker_mac_address
        self.sink_name = sink_name
        self.queue = []

        self.start_speech_callback = None
        self.end_speech_callback = None

    def write(self, contents):
        string = '.'.join([c.body for c in contents if isinstance(c, TextContent)]).replace('\n', '')

        logging.debug(u'Adding to queue: {}'.format(string))

        file_path = 'static/speech/{}.mp3'.format(str(uuid4()))
        text_to_speech(string=string, file_path=file_path)

        logging.debug('Done with text_to_speech')

        self.queue.append(file_path)

        logging.debug('Added to queue')

    def get_worker(self):

        def worker():
            while True:
                # Play first item in the queue
                if len(self.queue) > 0:
                    self._play_speech(self.queue.pop(0))

        return Thread(target=infinite_worker(worker), name='Speech output')

    def _play_speech(self, file_path):
        if self.start_speech_callback:
            self.start_speech_callback()

        pair_speaker(mac_address=self.speaker_mac_address, sink_name=self.sink_name)

        play_mp3('assets/speech-announcement.mp3')
        play_mp3(file_path)

        os.remove(file_path)

        if self.end_speech_callback:
            self.end_speech_callback()
