from datetime import datetime

from utils.content import TextContent
from utils.script import Script


class CurrentTimeScript(Script):

    def run(self, input_content):

        formatted_time = datetime.now().strftime('%I:%M%p')
        self.output([TextContent('It is {}'.format(formatted_time))])
