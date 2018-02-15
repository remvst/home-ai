import json
import logging
import os
from threading import Thread

from flask import request
from kik import Configuration
from kik.messages import TextMessage, messages_from_json
from werkzeug.serving import run_simple

from utils.content import TextContent
from utils.infinite_worker import infinite_worker


def get_worker(web_app, port, kik, response_set, recipient_username):

    def worker():
        run_simple('localhost', port, web_app)

    def messages_handler(messages):
        for message in messages:
            if message.from_user != recipient_username:
                continue

            if not isinstance(message, TextMessage):
                continue

            content = TextContent(body=message.body)

            response_set.maybe_handle(content)

    @web_app.route('/', methods=['POST'])
    def incoming_messages():
        signature = request.headers.get('X-Kik-Signature')
        raw_body = request.get_data()

        if not kik.verify_signature(signature, raw_body):
            return '', 403

        json_body = json.loads(raw_body)
        messages = messages_from_json(json_body['messages'])

        logging.debug(messages)

        # Handle the message in a different thread so we can return a 200 right away
        Thread(target=messages_handler, args=[messages]).start()

        return '', 200

    return Thread(target=infinite_worker(worker), name='Web server')
