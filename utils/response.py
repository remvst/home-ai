class Response(object):

    def __init__(self, label, command, output):
        super(Response, self).__init__()

        self.label = label
        self.command = command
        self.output = output

    def respond(self, input):
        raise Exception('Must implement respond()')
