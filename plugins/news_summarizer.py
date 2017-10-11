import httplib2
import json
import os
from datetime import date, datetime, time, timedelta
from dateutil import parser

from lib.text_plugin import TextPlugin

class NewsSummarizer(TextPlugin):

    def __init__(self, api_key, sources):
        super(NewsSummarizer, self).__init__()

        self.api_key = api_key
        self.sources = sources

    def fetch_articles(self, source):
        url = 'https://newsapi.org/v1/articles?source={}&sortBy={}&apiKey={}'.format(
            source,
            'top',
            self.api_key
        )

        http = httplib2.Http()
        resp, content = http.request(url)

        assert resp.status == 200

        return json.loads(content)['articles'][:5]

    def generate(self):
        lines = ['Here are the headlines for today']
        for source in self.sources:
            try:
                lines.append('In {}'.format(source))
                articles = self.fetch_articles(source)
                lines.extend([article['title'] for article in articles])
            except Exception as ex:
                logging.exception(ex)
                return 'Error getting {} news headlines'.format(source)

        return '. '.join(lines)
