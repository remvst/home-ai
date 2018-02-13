class Content(object):
    pass


class TextContent(Content):

    def __init__(self, body):
        super(TextContent, self).__init__()
        self.body = body

    def __str__(self):
        return self.body


class URLContent(Content):

    def __init__(self, url):
        super(TextContent, self).__init__()
        self.url = url

    def __str__(self):
        return self.url
