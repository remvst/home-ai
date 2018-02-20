import config
from plugins.news_summarizer import NewsSummarizer
from utils.content import URLContent, TextContent
from utils.script import Script


class HeadlinesScript(Script):

    def run(self, input_content):
        news_summarizer = NewsSummarizer(
            api_key=config.NEWS_API_KEY,
            sources=['bbc-news']
        )
        self.output([TextContent(news_summarizer.generate_string())])


class HeadlinesLinksScript(Script):

    def run(self, input_content):
        news_summarizer = NewsSummarizer(
            api_key=config.NEWS_API_KEY,
            sources=['bbc-news']
        )
        self.output([URLContent(url=url) for url in news_summarizer.generate_urls()])
