import copy
from threading import Thread

from utils.content import TextContent
from utils.output import BufferOutput


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

    @staticmethod
    def _thread(script, input_content, output):

        def worker():
            script.outputting_to(output).run(input_content)

        return Thread(target=worker)

    def run(self, input_content):
        # Create one buffer for each thread to output to
        buffers = [BufferOutput() for _ in xrange(len(self.scripts))]

        # Create each thread
        threads = []
        for i in xrange(len(self.scripts)):
            threads.append(self._thread(self.scripts[i], input_content, buffers[i]))

        # Run all the threads in parallel
        for thread in threads:
            thread.start()

        # Wait for them to finish
        for thread in threads:
            thread.join()

        # Join all the buffers
        overall_buffer = []
        for buffer_output in buffers:
            overall_buffer.extend(buffer_output.buffer)

        # Send the entire batch to the output
        self.output(overall_buffer)

    def outputting_to(self, output_stream):
        return CompositeScript(scripts=[script.outputting_to(output_stream) for script in self.scripts])


class ParallelScript(Script):

    def __init__(self, scripts):
        super(ParallelScript, self).__init__()
        self.scripts = scripts

    @staticmethod
    def _thread(script, input_content):

        def worker():
            script.run(input_content)

        return Thread(target=worker)

    def run(self, input_content):
        threads = [self._thread(script, input_content) for script in self.scripts]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def outputting_to(self, output_stream):
        return ParallelScript(scripts=[script.outputting_to(output_stream) for script in self.scripts])


class EchoScript(Script):

    def run(self, input_content):
        self.output([input_content])


class EchoTextScript(Script):

    def __init__(self, echo_format='{}'):
        super(EchoTextScript, self).__init__()
        self.echo_format = echo_format

    def run(self, input_content):
        if not isinstance(input_content, TextContent):
            return

        self.output([TextContent(body=self.echo_format.format(input_content.body))])
