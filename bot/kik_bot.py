from kik import KikApi, Configuration
from kik.messages import LinkMessage, PictureMessage, SuggestedResponseKeyboard, TextMessage, TextResponse, messages_from_json

import config
from utils.content import TextContent, URLContent, PictureURLContent
from utils.output import Output
from utils.response import ResponseSet

class KikBotOutput(Output):

    def __init__(self, kik, default_keyboard=None):
        self.kik = kik

        self.default_keyboard = default_keyboard

    def content_to_message(self, content):
        if isinstance(content, TextContent):
            return TextMessage(body=content.body, to=config.KIK_BOT_RECIPIENT_USERNAME)

        if isinstance(content, URLContent):
            return LinkMessage(url=content.url)

        if isinstance(content, PictureURLContent):
            return PictureMessage(pic_url=content.picture_url)

        raise Exception('Unrecognized content type')

    def output(self, contents):
        messages = [self.content_to_message(content) for content in contents]

        for message in messages:
            message.keyboards = [self.default_keyboard]

        self.kik.send_messages(messages)

    def update_config(self, webhook):
        self.config.webhook = webhook
        self.kik.set_configuration(self.config)
