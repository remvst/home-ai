import sys

from utils.content import TextContent
from utils.script import Script


class ExitProcessScript(Script):

    def run(self, input_content):
        self.output([TextContent(body='Killing process')])
        sys.exit(0)
