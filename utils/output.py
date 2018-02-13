import logging


class Output(object):

    def output(self):
        pass


class LogOutput(Output):

    def output(self, contents):
        for content in contents:
            logging.debug(str(content))


class MultiOutput(Output):

    def __init__(self, outputs, *args, **kwargs):
        super(MultiOutput, self).__init__(*args, **kwargs)
        self.outputs = outputs

    def output(self, contents):
        for output in self.outputs:
            output.output(contents)
