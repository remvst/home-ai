import config
from plugins.news_summarizer import NewsSummarizer
from utils.content import TextContent
from utils.script import Script


class HeadlinesScript(Script):

    def run(self, input_content):
        news_summarizer = NewsSummarizer(
            api_key=config.NEWS_API_KEY,
            sources=['bbc-news']
        )
        self.output([TextContent(news_summarizer.generate_string())])
