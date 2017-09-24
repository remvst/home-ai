from datetime import datetime

from lib.text_plugin import TextPlugin

class TimeAnnouncer(TextPlugin):

    def generate(self):
        formatted_time = datetime.now().strftime('%I:%M%p')
        return 'It is {}'.format(formatted_time)
