from utils.content import TextContent
from utils.response import Response


class AlarmResponse(Response):

    def respond(self, input):
        self.output.output(TextContent('This is an alarm'))
