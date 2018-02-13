from kik import KikApi, Configuration
from kik.messages import LinkMessage, PictureMessage, SuggestedResponseKeyboard, TextMessage, TextResponse, messages_from_json

import config
from helpers.video_surveillance import VideoSurveillance
from scripts.good_morning import generate_string as good_morning
from utils.content import TextContent, URLContent
from utils.output import Output

class KikBot(Output):

    def __init__(self, responses):
        super(KikBot, self).__init__()
        self.responses = responses

        self.kik = KikApi(config.KIK_BOT_USERNAME, config.KIK_BOT_API_KEY)
        self.config = Configuration(webhook=None)

    def update_config(self, webhook):
        self.config.webhook = webhook
        self.kik.set_configuration(self.config)

    def default_keyboard(self):
        responses = [r.label for r in self.responses]
        return SuggestedResponseKeyboard(responses=responses)

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
            message.keyboards = [keyboard]

        self.kik.send_messages(messages)

    def handle_messages(self, messages):
        for message in messages:
            if message.from_user != config.KIK_BOT_RECIPIENT_USERNAME:
                continue

            if not isinstance(message, TextMessage):
                continue

            content = TextContent(body=message.body)

            for response in self.responses:
                response.maybe_handle(content)


bot = KikBot()
