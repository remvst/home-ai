class Response(object):

    def __init__(self, label, command, script):
        super(Response, self).__init__()

        self.label = label
        self.command = command
        self.script = script

    def respond(self, input_content):
        self.script.run(input_content)

    def maybe_handle(self, input_content):
        if not self.command.matches(input_content):
            return False

        self.respond(input_content)
        return True


class ResponseSet(object):

    def __init__(self, responses):
        super(ResponseSet, self).__init__()
        self.responses = responses

    def maybe_handle(self, content):
        for response in self.responses:
            if response.maybe_handle(content):
                return True

        return False
