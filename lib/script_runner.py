import threading

from lib.handler import Handler
from output.stdout import Stdout


class ScriptRunner(Handler):

    def __init__(self, script, output=Stdout()):
        super(ScriptRunner, self).__init__()

        self.script = script
        self.output = output

    def run(self):
        self.output.output(self.script.generate())

    def run_in_parallel(self):
        thread = threading.Thread(target=self.run)
        thread.start()
