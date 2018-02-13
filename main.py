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
from kik.messages import SuggestedResponseKeyboard, TextResponse

import config
from bot.kik_bot import KikBotOutput
from scripts.get_tunnel_url import GetTunnelURLScript
from scripts.good_morning import GoodMorningScript
from scripts.take_picture import TakePictureScript
from utils.command import AnyCommand, TextCommand
from utils.output import MultiOutput
from utils.response import Response, ResponseSet
from utils.script import CompositeScript, EchoScript, StaticTextScript
from utils.sound import play_mp3, pair_speaker
from workers.alarm_clock import get_worker as generate_alarm_worker
from workers.ngrok import get_worker as generate_ngrok_worker
from workers.speech import SpeechOutput
from workers.voice import get_worker as generate_voice_worker
from workers.web_server import get_worker as generate_web_worker

logging.getLogger().setLevel(logging.DEBUG)

# Check if super user (if yes, GTFO)
if os.geteuid() == 0:
    logging.error('This is not meant to be run as root')
    sys.exit(1)

# Outputs
kik = KikApi(config.KIK_BOT_USERNAME, config.KIK_BOT_API_KEY)
bot_output = KikBotOutput(kik=kik, default_keyboard=SuggestedResponseKeyboard(
    responses=[
        TextResponse('Check Running'),
        TextResponse('Tunnel URL'),
        TextResponse('Alarm Clock'),
        TextResponse('Picture')
    ]
))

speech_output = SpeechOutput(speaker_mac_address=config.SPEAKER_MAC_ADDRESS,
                             sink_name=config.SINK_NAME)

static_folder = '{}/{}'.format(os.path.dirname(os.path.abspath(__file__)), 'static')
web_app = Flask(__name__, static_folder=static_folder)

bot_and_speech_output = MultiOutput(outputs=[speech_output, bot_output])

# Scripts
good_morning_script = GoodMorningScript()
take_picture_script = TakePictureScript(static_folder=static_folder)
get_tunnel_url_script = GetTunnelURLScript()
running_script = StaticTextScript(body='I am running indeed')

# Responders
bot_response = ResponseSet(responses=[
    Response(
        label='Check running',
        command=TextCommand(keywords=['check']),
        script=running_script,
        output=bot_and_speech_output
    ),
    Response(
        label='Alarm',
        command=TextCommand(keywords=['alarm', 'clock', 'morning']),
        script=good_morning_script,
        output=speech_output
    ),
    Response(
        label='Picture',
        command=TextCommand(keywords=['picture']),
        script=take_picture_script,
        output=bot_output
    ),
    Response(
        label='Tunnel URL',
        command=TextCommand(keywords=['tunnel']),
        script=get_tunnel_url_script,
        output=bot_output
    ),
    Response(
        label='Default',
        command=AnyCommand(),
        script=CompositeScript(scripts=[
            StaticTextScript(body='Unrecognized command'),
            EchoScript()
        ]),
        output=bot_output
    )
])

voice_response = ResponseSet(responses=[
    Response(
        label='Alarm',
        command=TextCommand(keywords=['alarm', 'clock', 'morning']),
        script=good_morning_script,
        output=speech_output
    ),
    Response(
        label='Picture',
        command=TextCommand(keywords=['picture']),
        script=take_picture_script,
        output=bot_output
    ),
    Response(
        label='Impress',
        command=TextCommand(keywords=['impress']),
        script=StaticTextScript(body='Hey Samantha are you Google? Cause you\'re everything I\'m looking for'),
        output=speech_output
    )
])

alarm_response = Response(
    label='Alarm',
    command=AnyCommand(),
    script=GoodMorningScript(),
    output=speech_output
)

# Workers
web_server = generate_web_worker(web_app=web_app, port=config.KIK_BOT_PORT, kik=kik,
                                 response_set=bot_response,
                                 recipient_username=config.KIK_BOT_RECIPIENT_USERNAME)
ngrok_worker = generate_ngrok_worker(port=config.KIK_BOT_PORT, kik=kik)
alarm_worker = generate_alarm_worker(response=alarm_response)
speech_worker = speech_output.get_worker()
voice_worker = generate_voice_worker(prefix='please', response=voice_response)

workers = [
    (web_server, 'Web server'),
    (ngrok_worker, 'ngrok'),
    (alarm_worker, 'Alarm clock'),
    (speech_worker, 'Speech output'),
    (voice_worker, 'Voice')
]

logging.debug('Starting threads')

def infinite_worker(worker):
    def new_worker():
        while True:
            try:
                worker()
            except Exception as e:
                logging.exception(e)
                logging.debug('Restarting thread in 5 seconds')
                sleep(5)
            finally:
                pass

    return new_worker

threads = []
for worker, name in workers:
    thread = threading.Thread(target=infinite_worker(worker), name=name)
    thread.daemon = True
    threads.append(thread)
    thread.start()

logging.debug('All threads started')

pair_speaker(mac_address=config.SPEAKER_MAC_ADDRESS, sink_name=config.SINK_NAME)
play_mp3('assets/initialized-home-ai.mp3')

# Prevent the main thread from dying
while threading.active_count() > 0:
    sleep(0.1)
