import json
import logging
import os

from flask import Flask, request
from kik.messages import messages_from_json
from werkzeug.serving import run_simple

import config
from bot.kik_bot import bot
from web.app import app

def worker():
    run_simple('localhost', config.KIK_BOT_PORT, app)

@app.route('/', methods=['POST'])
def incoming_messages():
    signature = request.headers.get('X-Kik-Signature')
    raw_body = request.get_data()

    if not bot.kik.verify_signature(signature, raw_body):
        return '', 403

    json_body = json.loads(raw_body)
    messages = messages_from_json(json_body['messages'])

    bot.handle_messages(messages)

    return '', 200
