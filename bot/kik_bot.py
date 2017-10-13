import logging
from datetime import datetime

from kik import KikApi, Configuration
from kik.messages import PictureMessage, SuggestedResponseKeyboard, TextMessage, TextResponse, messages_from_json

import config
from scripts.good_morning import generate_string as good_morning
from utils.camera import take_picture
from utils.ngrok import get_ngrok_url
from utils.process import restart_process
from web.app import app, path_to_static_file
from workers.speech import add_to_queue

class KikBot(object):

    def __init__(self, default_keyboard=None):
        super(KikBot, self).__init__()
        self.kik = KikApi(config.KIK_BOT_USERNAME, config.KIK_BOT_API_KEY)
        self.config = Configuration(webhook=None)

    def send(self, messages):
        # Add suggested responses to all messages
        for message in messages:
            message.keyboards = [
                SuggestedResponseKeyboard(responses=[
                    TextResponse('Check Running'),
                    TextResponse('Tunnel URL'),
                    TextResponse('Alarm'),
                    TextResponse('Restart'),
                    TextResponse('Picture'),
                    TextResponse('Surveillance')
                ])
            ]

        try:
            self.kik.send_messages(messages)
        except Exception as e:
            logging.exception(e)

    def update_config(self, webhook):
        self.config.webhook = webhook
        self.kik.set_configuration(self.config)

    def handle_messages(self, messages):
        for message in messages:
            if message.from_user != 'remvst':
                continue

            if isinstance(message, TextMessage):
                self.handle_text_message(message)

    def handle_text_message(self, message):
        body = message.body.lower()

        if 'alarm' in body:
            string = good_morning()
            add_to_queue(string)
            self.send([TextMessage(body='Playing alarm', to=message.from_user)])
            return

        if 'tunnel' in body:
            self.send([TextMessage(body=get_ngrok_url(), to=message.from_user)])
            return

        if 'kill' in body:
            self.send([TextMessage(body='Terminating process', to=message.from_user)])
            exit(1)
            return

        if 'restart' in body:
            self.send([TextMessage(body='Restarting process', to=message.from_user)])
            restart_process()
            return

        if 'picture' in body:
            now = datetime.utcnow()
            pic_id = now.isoformat()

            relative_path = '{}/pictures/{}.png'.format(app.static_folder, pic_id)
            take_picture(relative_path)

            url = '{}/{}'.format(get_ngrok_url(), path_to_static_file(relative_path))
            self.send([PictureMessage(pic_url=url, to=message.from_user)])
            return

        add_to_queue(body)
        self.send([TextMessage(body='Playing on speaker', to=message.from_user)])


bot = KikBot()
