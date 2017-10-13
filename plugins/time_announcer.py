from datetime import datetime

from plugins.text_plugin import TextPlugin

class TimeAnnouncer(TextPlugin):

    def generate_string(self):
        formatted_time = datetime.now().strftime('%I:%M%p')
        return 'It is {}'.format(formatted_time)
