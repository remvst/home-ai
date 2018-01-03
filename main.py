import logging
import os
import StringIO
import subprocess
import sys
import threading
from datetime import time
from time import sleep

import config
from utils.infinite_thread import InfiniteThread
from workers.alarm_clock import worker as alarm_clock
from workers.clapclap import worker as clapclap
from workers.ngrok import worker as ngrok
from workers.web_server import worker as web_server
from workers.speech import worker as speech, add_to_queue
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
    (clapclap, 'Clap clap detector')
]

logging.debug('Starting threads')

threads = []
for worker, name in workers:
    def crash_handler(exception, description):
        message = 'Thread crashed: {}'.format(description)
        logging.exception(exception)

    thread = InfiniteThread(target=worker, name=name, crash_handler=crash_handler)
    thread.daemon = True
    threads.append(thread)
    thread.start()

logging.debug('All threads started')

add_to_queue('Initialized home AI')

# Prevent the main thread from dying
while threading.active_count() > 0:
    sleep(0.1)
