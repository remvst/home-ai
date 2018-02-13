class Response(object):

    def __init__(self, label, command, script, output):
        super(Response, self).__init__()

        self.label = label
        self.command = command
        self.output = output
        self.script = script

    def respond(self, input):
        self.script.run(input, self.output)

    def maybe_handle(self, input):
        if not self.command.matches(input):
            return False

        self.respond(input)
        return True


class ResponseSet(object): # TODO fix inheritance

    def __init__(self, responses, *args, **kwargs):
        super(ResponseSet, self).__init__(*args, **kwargs)
        self.responses = responses

    def maybe_handle(self, content):
        for response in self.responses:
            if response.maybe_handle(content):
                return True

        return False
