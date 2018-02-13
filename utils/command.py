class Command(object):

    def __init__(self, keywords):
        super(Command, self).__init__()
        self.keywords = keywords

    def matches(self, text):
        text = text.lower()

        for keyword in self.keywords:
            if keyword.lower() in text:
                return True

        return False
