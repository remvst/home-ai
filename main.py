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
from workers.voice import get_workers as generate_voice_workers
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
logging.debug('Starting threads')

voice_input_process, voice_processing_thread = generate_voice_workers(prefix='please', response=voice_response)

threads = [
    generate_web_worker(web_app=web_app, port=config.KIK_BOT_PORT, kik=kik,
                        response_set=bot_response,
                        recipient_username=config.KIK_BOT_RECIPIENT_USERNAME),
    generate_ngrok_worker(port=config.KIK_BOT_PORT, kik=kik),
    generate_alarm_worker(response=alarm_response),
    speech_output.get_worker(),
    voice_processing_thread
]

for thread in threads:
    thread.start()

logging.debug('All threads started')

# Starting voice input process
voice_input_process.start()

pair_speaker(mac_address=config.SPEAKER_MAC_ADDRESS, sink_name=config.SINK_NAME)
play_mp3('assets/initialized-home-ai.mp3')

for thread in threads:
    thread.join()
