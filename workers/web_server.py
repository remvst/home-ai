import json
import logging
import os
import threading

from flask import Flask, request
from kik.messages import messages_from_json
from werkzeug.serving import run_simple

import config
from bot.kik_bot import KikBotOutput
from responses.alarm_response import AlarmResponse
from utils.command import TextCommand
from utils.response import Response, ResponseSet
from web.app import app

kik = KikApi(config.KIK_BOT_USERNAME, config.KIK_BOT_API_KEY)
config = Configuration(webhook=None)

bot_output = KikBotOutput(kik=kik)

response_set = ResponseSet(responses=[
    AlarmResponse(
        label='Alarm',
        command=TextCommand(keywords=['alarm', 'clock']),
        output=bot_output
    )
])

def worker():
    run_simple('localhost', config.KIK_BOT_PORT, app)

def update_config():
    config.webhook = webhook
    kik.set_configuration(config)

@app.route('/', methods=['POST'])
def incoming_messages():
    signature = request.headers.get('X-Kik-Signature')
    raw_body = request.get_data()

    if not kik.verify_signature(signature, raw_body):
        return '', 403

    json_body = json.loads(raw_body)
    messages = messages_from_json(json_body['messages'])

    def worker():
        for message in messages:
            if message.from_user != config.KIK_BOT_RECIPIENT_USERNAME:
                continue

            if not isinstance(message, TextMessage):
                continue

            content = TextContent(body=message.body)




    threading.Thread(target=worker).start()

    return '', 200
