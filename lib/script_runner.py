from lib.handler import Handler

class ScriptRunner(Handler):

    def __init__(self, script):
        super(ScriptRunner, self).__init__()

        self.script = script

    def run(self):
        print(self.script.generate())
