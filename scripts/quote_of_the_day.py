from plugins.quote_of_the_day import QuoteOfTheDay
from utils.content import TextContent
from utils.script import Script


class QuoteOfTheDayScript(Script):

    def run(self, input_content):
        quote_of_the_day = QuoteOfTheDay()

        self.output([TextContent(quote_of_the_day.generate_string())])
