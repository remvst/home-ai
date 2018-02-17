import copy

from utils.content import TextContent


class Script(object):

    def __init__(self, output=None):
        super(Script, self).__init__()
        self.output_stream = output

    def run(self, input_content):
        raise Exception('Must implement run() method')

    def output(self, content):
        if self.output_stream is None:
            return

        self.output_stream.write(content)

    def outputting_to(self, output_stream):
        copied_script = copy.copy(self)
        copied_script.output_stream = output_stream
        return copied_script


class StaticTextScript(Script):

    def __init__(self, body):
        super(StaticTextScript, self).__init__()
        self.body = body

    def run(self, input_content):
        self.output([TextContent(body=self.body)])


class CompositeScript(Script):

    def __init__(self, scripts):
        super(CompositeScript, self).__init__()
        self.scripts = scripts

    def run(self, input_content):
        for script in self.scripts:
            script.run(input_content)

    def outputting_to(self, output_stream):
        return CompositeScript(scripts=[script.outputting_to(output_stream) for script in self.scripts])


class EchoScript(Script):

    def run(self, input_content):
        self.output([input_content])
