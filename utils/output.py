import logging


class Output(object):

    def output(self):
        pass


class LogOutput(Output):

    def output(self, contents):
        for content in contents:
            logging.debug(str(content))
