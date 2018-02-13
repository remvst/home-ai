import logging
import os
import StringIO
import subprocess
import sys
import threading
from datetime import time
from time import sleep

from flask import Flask
from kik import KikApi

import config
from bot.kik_bot import KikBotOutput
from scripts.good_morning import GoodMorningScript
from utils.command import TextCommand
from utils.response import Response, ResponseSet
from utils.sound import play_mp3, pair_speaker
# from workers.alarm_clock import worker as alarm_clock
# from workers.ngrok import worker as ngrok
# from workers.speech import worker as speech
# from workers.speech_tests import worker as speech_tests
# from workers.surveillance import worker as surveillance
from workers.web_server import get_worker as generate_web_worker

logging.getLogger().setLevel(logging.DEBUG)

# Check if super user (if yes, GTFO)
if os.geteuid() == 0:
    logging.error('This is not meant to be run as root')
    sys.exit(1)

kik = KikApi(config.KIK_BOT_USERNAME, config.KIK_BOT_API_KEY)
bot_output = KikBotOutput(kik=kik)

static_folder = '{}/{}'.format(os.path.dirname(os.path.abspath(__file__)), '../static')
web_app = Flask(__name__, static_folder=static_folder)

bot_response_set = ResponseSet(responses=[
    Response(
        label='Alarm',
        command=TextCommand(keywords=['alarm', 'clock', 'morning']),
        script=GoodMorningScript(),
        output=bot_output
    )
])

web_server = generate_web_worker(
    web_app=web_app,
    kik=kik,
    response_set=bot_response_set
)

# workers = [
#     # (surveillance, 'Surveillance'),
#     (alarm_clock, 'Alarm clock'),
#     (speech, 'Speech queue'),
#     (ngrok, 'ngrok'),
#     (web_server, 'Web server'),
#     (speech_tests, 'Speech tests')
# ]

workers = [
    (web_server, 'Web server')
]

logging.debug('Starting threads')

threads = []
for worker, name in workers:
    thread = threading.Thread(target=worker, name=name)
    thread.daemon = True
    threads.append(thread)
    thread.start()

logging.debug('All threads started')

# pair_speaker(mac_address=config.SPEAKER_MAC_ADDRESS, sink_name=config.SINK_NAME)
play_mp3('assets/initialized-home-ai.mp3')

# Prevent the main thread from dying
while threading.active_count() > 0:
    sleep(0.1)
