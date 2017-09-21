from lib.text_plugin import TextPlugin

class GoodMorning(TextPlugin):

    def __init__(self, name):
        super(GoodMorning, self).__init__()

        self.name = name

    def generate(self):
        return 'good morning {}'.format(self.name)
