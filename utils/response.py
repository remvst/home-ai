class Response(object):

    def __init__(self, label, command, output):
        super(Response, self).__init__()

        self.label = label
        self.command = command
        self.output = output

    def respond(self, input):
        raise Exception('Must implement respond()')

    def maybe_handle(self, input):
        if not self.command.matches(input):
            return False

        self.respond(input)
        return True


def ResponseSet(Response):

    def __init__(self, responses):
        super(ResponseSet, self).__init__()
        self.responses = responses

        self.output = KikBotOutput(self.kik)

    def maybe_handle(self, content):
        for response in self.responses:
            if response.maybe_handle(content):
                break
