from lib.utils import say
from output import Output


class Speech(Output):

    def output(self, string):
        say(string)
