import logging
from datetime import datetime

from kik import KikApi, Configuration
from kik.messages import PictureMessage, SuggestedResponseKeyboard, TextMessage, TextResponse, messages_from_json

import config
from helpers.video_surveillance import VideoSurveillance
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
                    TextResponse('Alarm Clock'),
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
            if message.from_user != config.KIK_BOT_RECIPIENT_USERNAME:
                continue

            if not isinstance(message, TextMessage):
                continue

            self.handle_text_message(message)

    def handle_text(self, text):
        text = text.lower()

        if 'alarm' in text and 'clock' in text:
            string = good_morning()
            add_to_queue(string)
            self.send([TextMessage(body='Playing alarm', to=config.KIK_BOT_RECIPIENT_USERNAME)])
            return True

        if 'tunnel' in text:
            self.send([TextMessage(body=get_ngrok_url(), to=config.KIK_BOT_RECIPIENT_USERNAME)])
            return True

        if 'kill' in text:
            self.send([TextMessage(body='Terminating process', to=config.KIK_BOT_RECIPIENT_USERNAME)])
            exit(1)
            return True

        if 'restart' in text:
            self.send([TextMessage(body='Restarting process', to=config.KIK_BOT_RECIPIENT_USERNAME)])
            restart_process()
            return True

        if 'picture' in text:
            now = datetime.utcnow()
            pic_id = now.isoformat()

            relative_path = '{}/pictures/{}.jpg'.format(app.static_folder, pic_id)
            take_picture(relative_path)

            url = '{}/{}'.format(get_ngrok_url(), path_to_static_file(relative_path))
            self.send([PictureMessage(pic_url=url, to=config.KIK_BOT_RECIPIENT_USERNAME)])
            return True

        if 'surveillance' in text:
            surveillance = VideoSurveillance(pictures_folder='{}/surveillance'.format(app.static_folder))
            picture_path, enhanced_path, detected = surveillance.survey()
            url = '{}/{}'.format(get_ngrok_url(), path_to_static_file(enhanced_path))
            self.send([PictureMessage(pic_url=url, to=config.KIK_BOT_RECIPIENT_USERNAME)])
            return True

        return False

    def handle_text_message(self, message):
        body = message.body.lower()

        if not self.handle_text(body):
            add_to_queue(body)
            self.send([TextMessage(body='Playing on speaker', to=config.KIK_BOT_RECIPIENT_USERNAME)])


bot = KikBot()
