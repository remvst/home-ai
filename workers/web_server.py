import json
import logging
import os
import threading

from flask import request
from kik import Configuration
from kik.messages import TextMessage, messages_from_json
from werkzeug.serving import run_simple

from utils.content import TextContent

def get_worker(web_app, port, kik, response_set, recipient_username):

    def worker():
        run_simple('localhost', port, web_app)

    @web_app.route('/', methods=['POST'])
    def incoming_messages():
        signature = request.headers.get('X-Kik-Signature')
        raw_body = request.get_data()

        if not kik.verify_signature(signature, raw_body):
            return '', 403

        json_body = json.loads(raw_body)
        messages = messages_from_json(json_body['messages'])

        def thread_handler():
            for message in messages:
                if message.from_user != recipient_username:
                    continue

                if not isinstance(message, TextMessage):
                    continue

                content = TextContent(body=message.body)

                response_set.maybe_handle(content)

        threading.Thread(target=thread_handler).start()

        return '', 200

    return worker
