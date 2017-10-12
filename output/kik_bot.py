import json
import logging
import os

from flask import Flask, request, send_from_directory, url_for
from kik import KikApi, Configuration
from kik.messages import PictureMessage, TextMessage, messages_from_json
from werkzeug.serving import run_simple

from output import Output


class KikBot(Output):

    def __init__(self, bot_username, bot_api_key, recipient_username, message_handler=None, default_keyboard=None, static_folder=None):
        super(KikBot, self).__init__()

        self.kik = KikApi(bot_username, bot_api_key)
        self.recipient_username = recipient_username
        self.message_handler = message_handler
        self.default_keyboard = default_keyboard
        self.static_folder = static_folder

        self.config = Configuration(webhook=None)

        self.flask_app = Flask(__name__, static_url_path='/static', static_folder=static_folder)

    def send(self, messages):
        for message in messages:
            message.keyboards = [self.default_keyboard]

        try:
            self.kik.send_messages(messages)
        except Exception as e:
            logging.exception(e)

    def output(self, string):
        self.send([
            TextMessage(
                to=self.recipient_username,
                body=string
            )
        ])

    def output_picture(self, url):
        self.send([
            PictureMessage(
                to=self.recipient_username,
                pic_url=url
            )
        ])

    def update_config(self, webhook):
        self.config.webhook = webhook
        self.kik.set_configuration(self.config)

    def http_worker(self, port):
        # Add the routes
        self.flask_app.add_url_rule(rule='/', methods=['POST'], view_func=self.incoming_messages)

        # And run the server!
        run_simple('localhost', port, self.flask_app)

    def incoming_messages(self):
        signature = request.headers.get('X-Kik-Signature')
        raw_body = request.get_data()

        if not self.kik.verify_signature(signature, raw_body):
            return '', 403

        json_body = json.loads(raw_body)
        messages = messages_from_json(json_body['messages'])

        # Send the messages to the outside handler
        if self.message_handler is not None:
            for message in messages:
                self.message_handler(message)

        return '', 200

    def path_to_static_file(self, relative_path):
        path_from_static = os.path.relpath(relative_path, self.static_folder)
        return 'static/{}'.format(path_from_static)
