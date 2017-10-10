import json

from flask import Flask, request
from kik import KikApi, Configuration
from kik.messages import TextMessage, messages_from_json
from werkzeug.serving import run_simple

from output import Output


class KikBot(Output):

    def __init__(self, bot_username, bot_api_key, recipient_username):
        super(KikBot, self).__init__()

        self.kik = KikApi(bot_username, bot_api_key)
        self.recipient_username = recipient_username

        self.config = Configuration(webhook=None)

        self.flask_app = Flask(__name__)

    def output(self, string):
        try:
            self.kik.send_messages([
                TextMessage(
                    to=self.recipient_username,
                    body=string
                )
            ])
        except Exception as e:
            print e

    def update_config(self, webhook):
        self.config.webhook = webhook
        self.kik.set_configuration(self.config)

    def http_worker(self, port):
        # Add the route the dirty way
        self.flask_app.route('/', methods=['POST'])(self.incoming_messages)

        # And run the server!
        run_simple('localhost', port, self.flask_app)

    def incoming_messages(self):
        signature = request.headers.get('X-Kik-Signature')
        raw_body = request.get_data()

        if not self.kik.verify_signature(signature, raw_body):
            return '', 403

        json_body = json.loads(raw_body)
        messages = messages_from_json(json_body['messages'])

        return '', 200
