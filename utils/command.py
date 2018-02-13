from utils.content import TextContent


class Command(object):

    def matches(self, input):
        raise Exception('Must implement matches() method')


class TextCommand(Command):

    def __init__(self, keywords):
        super(Command, self).__init__()
        self.keywords = keywords

    def matches(self, input):
        if not isinstance(input, TextContent):
            return

        text = input.body.lower()

        for keyword in self.keywords:
            if keyword.lower() in text:
                return True

        return False
