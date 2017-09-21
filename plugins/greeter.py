from lib.text_plugin import TextPlugin

class Greeter(TextPlugin):

    def __init__(self, name):
        super(Greeter, self).__init__()

        self.name = name

    def generate(self):
        return 'good morning {}'.format(self.name)
