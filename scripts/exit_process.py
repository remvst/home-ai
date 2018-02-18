import sys

from utils.content import TextContent
from utils.script import Script


class ExitProcessScript(Script):

    def __init__(self, exit_code):
        super(ExitProcessScript, self).__init__()
        self.exit_code = exit_code

    def run(self, input_content):
        self.output([TextContent(body='Killing process')])
        sys.exit(self.exit_code)
