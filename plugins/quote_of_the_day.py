import httplib2
import json

from lib.text_plugin import TextPlugin

class QuoteOfTheDay(TextPlugin):

    def fetch_quote(self):
        url = 'https://quotes.rest/qod'

        headers = {
            'Accept': 'application/json'
        }

        http = httplib2.Http()
        resp, content = http.request(url, headers=headers)

        assert resp.status == 200

        return json.loads(content)

    def generate(self):
        try:
            quote_data = self.fetch_quote()
        except:
            return 'Error fetching quote of the day'

        return 'Quote of the day by {}: {}'.format(
            quote_data['contents']['quotes'][0]['author'],
            quote_data['contents']['quotes'][0]['quote']
        )
