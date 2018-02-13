import json
import logging
import os
import threading

from flask import request
from kik import Configuration
from kik.messages import messages_from_json
from werkzeug.serving import run_simple

import config

def get_worker(web_app, kik, response_set):

    def update_config():
        kik.set_configuration(Configuration(webhook=webhook))

    def worker():
        run_simple('localhost', config.KIK_BOT_PORT, web_app)

    @web_app.route('/', methods=['POST'])
    def incoming_messages():
        signature = request.headers.get('X-Kik-Signature')
        raw_body = request.get_data()

        if not kik.verify_signature(signature, raw_body):
            return '', 403

        json_body = json.loads(raw_body)
        messages = messages_from_json(json_body['messages'])

        for message in messages:
            if message.from_user != config.KIK_BOT_RECIPIENT_USERNAME:
                continue

            if not isinstance(message, TextMessage):
                continue

            content = TextContent(body=message.body)

        return '', 200

    return worker
