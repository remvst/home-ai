import logging

from kik import KikApi, Configuration
from kik.messages import PictureMessage, TextMessage, messages_from_json

import config
from scripts.good_morning import generate_string as good_morning
from utils.camera import take_picture
from utils.ngrok import get_ngrok_url
from utils.process import restart_process
from workers.speech import add_to_queue
from workers.web_server import path_to_static_file

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
            if isinstance(message, TextMessage):
                self.handle_text_message(message)

    def handle_text_message(self, message):
        body = message.body.lower()

        # if 'check' in body:
        #     status_message = '\n'.join(['{}: {}'.format(thread.name, 'running' if thread.isAlive() else 'crashed') for thread in threads])
        #     bot_output.output(status_message)
        #     return

        if 'alarm' in body:
            string = good_morning()
            add_to_queue(string)
            send([TextMessage(body='Playing alarm', to=message.from_user)])
            return

        if 'tunnel' in body:
            send([TextMessage(body=get_ngrok_url(), to=message.from_user)])
            return

        if 'kill' in body:
            send([TextMessage(body='Terminating process', to=message.from_user)])
            exit(1)
            return

        if 'restart' in body:
            send([TextMessage(body='Restarting process', to=message.from_user)])
            restart_process()
            return

        if 'picture' in body:
            relative_path = '{}/pictures/my-pic.png'.format(bot_output.static_folder)
            take_picture(relative_path)

            url = '{}/{}'.format(get_ngrok_url(), path_to_static_file(relative_path))
            send([PictureMessage(pic_url=url, to=message.from_user)])
            return

        if 'surveillance' in body:
            picture_path, enhanced_path, detected = visual_home_check.survey()
            url = '{}/{}'.format(get_ngrok_url(), bot_output.path_to_static_file(enhanced_path))
            bot_output.output_picture(url)

            os.remove(picture_path)
            os.remove(enhanced_path)
            return

        speech_output.output(body)
        bot_output.output('Playing on speaker')


bot = KikBot()
