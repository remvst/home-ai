class Script(object):

    def run(self, input, output):
        raise Exception('Must implement run() method')


class CompositeScript(Script):

    def __init__(self, scripts, *args, **kwargs):
        super(CompositeScript, self).__init__(*args, **kwargs)
        self.scripts = scripts

    def run(self, input, output):
        for script in self.scripts:
            script.run(input, output)
