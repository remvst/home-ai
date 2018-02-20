import logging
from threading import Thread


class Output(object):

    def write(self, contents):
        pass


class BufferOutput(Output):

    def __init__(self):
        super(BufferOutput, self).__init__()
        self.buffer = []

    def write(self, contents):
        self.buffer.extend(contents)


class LogOutput(Output):

    def write(self, contents):
        for content in contents:
            logging.debug(str(content))


class MultiOutput(Output):

    def __init__(self, outputs):
        super(MultiOutput, self).__init__()
        self.outputs = outputs

    def write(self, contents):
        for output in self.outputs:
            output.write(contents)


class ThreadedOutput(Output):

    def __init__(self, output):
        super(ThreadedOutput, self).__init__()
        self.output = output

    def write(self, contents):
        def worker():
            self.output.write(contents)

        thread = Thread(target=worker)
        thread.daemon = True
        thread.start()