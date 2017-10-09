from kik import KikApi
from kik.messages import TextMessage

from output import Output


class KikBot(Output):

    def __init__(self, bot_username, bot_api_key, recipient_username):
        super(KikBot, self).__init__()

        self.kik = KikApi(bot_username, bot_api_key)
        self.recipient_username = recipient_username

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
