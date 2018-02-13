import logging
import os
import StringIO
import subprocess
import sys
import threading
from datetime import time
from time import sleep

import config
from utils.sound import play_mp3, pair_speaker
from workers.alarm_clock import worker as alarm_clock
from workers.ngrok import worker as ngrok
from workers.web_server import worker as web_server
from workers.speech import worker as speech
from workers.speech_tests import worker as speech_tests
from workers.surveillance import worker as surveillance

logging.getLogger().setLevel(logging.DEBUG)

# Check if super user (if yes, GTFO)
if os.geteuid() == 0:
    logging.error('This is not meant to be run as root')
    sys.exit(1)

workers = [
    # (surveillance, 'Surveillance'),
    (alarm_clock, 'Alarm clock'),
    (speech, 'Speech queue'),
    (ngrok, 'ngrok'),
    (web_server, 'Web server'),
    (speech_tests, 'Speech tests')
]

logging.debug('Starting threads')

threads = []
for worker, name in workers:
    thread = threading.Thread(target=worker, name=name)
    thread.daemon = True
    threads.append(thread)
    thread.start()

logging.debug('All threads started')

pair_speaker(mac_address=config.SPEAKER_MAC_ADDRESS, sink_name=config.SINK_NAME)
play_mp3('assets/initialized-home-ai.mp3')

# Prevent the main thread from dying
while threading.active_count() > 0:
    sleep(0.1)
