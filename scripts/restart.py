from time import sleep

from utils.content import TextContent
from utils.process import restart_process
from utils.script import Script


class RestartScript(Script):

    def __init__(self, *args, **kwargs):
        super(TakePictureScript, self).__init__(*args, **kwargs)

    def run(self, input, output):
        output.output([TextContent(body='Restarting in 5 seconds')])

        sleep(2)

        restart_process()
