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
