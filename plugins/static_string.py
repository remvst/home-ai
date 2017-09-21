from lib.text_plugin import TextPlugin

class StaticString(TextPlugin):

    def __init__(self, string):
        super(StaticString, self).__init__()

        self.string = string

    def generate(self):
        return self.string
