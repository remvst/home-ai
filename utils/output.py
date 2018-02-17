import logging


class Output(object):

    def write(self, contents):
        pass


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
