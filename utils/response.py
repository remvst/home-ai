class Response(object):

    def __init__(self, label, command, script):
        super(Response, self).__init__()

        self.label = label
        self.command = command
        self.script = script

    def should_handle(self, input_content):
        return self.command.matches(input_content)

    def maybe_handle(self, input_content):
        if not self.should_handle(input_content):
            return False

        self.script.run(input_content)
        return True


class ResponseSet(object):

    def __init__(self, responses, confused_script=None):
        super(ResponseSet, self).__init__()
        self.responses = responses
        self.confused_script = confused_script

    def _handling_responses(self, input_content):
        return [response for response in self.responses if response.should_handle(input_content)]

    def should_handle(self, input_content):
        return len(self.handling_responses(input_content)) > 0

    def maybe_handle(self, input_content):
        responses = self._handling_responses(input_content)

        if len(responses) == 0:
            return False

        if len(responses) > 1 and self.confused_script is not None:
            # Several responses, we're confused
            self.confused_script.run(input_content)
            return True

        responses[0].maybe_handle(input_content)
        return True
