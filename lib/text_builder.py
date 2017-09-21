class TextBuilder(object):

    def __init__(self):
        super(TextBuilder, self).__init__()

        self.text_plugins = []

    def add_text_plugin(self, text_plugin):
        self.text_plugins.append(text_plugin)

    def generate(self):
        return '. '.join(plugin.generate() for plugin in self.text_plugins)
