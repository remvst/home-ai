from utils.content import TextContent


class Script(object):

    def run(self, input, output):
        raise Exception('Must implement run() method')


class StaticTextScript(object):

    def __init__(self, body, *args, **kwargs):
        super(StaticTextScript, self).__init__(*args, **kwargs)
        self.body = body

    def run(self, input, output):
        output.output([TextContent(body=self.body)])


class CompositeScript(Script):

    def __init__(self, scripts, *args, **kwargs):
        super(CompositeScript, self).__init__(*args, **kwargs)
        self.scripts = scripts

    def run(self, input, output):
        for script in self.scripts:
            script.run(input, output)


class EchoScript(Script):

    def run(self, input, output):
        output.output([input])
