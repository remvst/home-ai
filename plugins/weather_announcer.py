import httplib2
import json

from plugins.text_plugin import TextPlugin

def to_celsius(kelvin_temperature):
    return kelvin_temperature - 273.15

class WeatherAnnouncer(TextPlugin):

    def __init__(self, api_key, location_query):
        super(WeatherAnnouncer, self).__init__()

        self.api_key = api_key
        self.location_query = location_query

    def fetch_weather(self):
        url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&APPID={}'.format(self.location_query, self.api_key)

        http = httplib2.Http()
        resp, content = http.request(url)

        assert resp.status == 200

        return json.loads(content)

    def generate_string(self):
        try:
            weather = self.fetch_weather()
            next_12_hours_data = weather['list'][:4] # chunks of 3 hours
        except:
            return 'Error fetching weather'

        min_temp = int(round(min(to_celsius(chunk['main']['temp_min']) for chunk in next_12_hours_data)))
        max_temp = int(round(max(to_celsius(chunk['main']['temp_max']) for chunk in next_12_hours_data)))

        weather_types = list(set([chunk['weather'][0]['description'] for chunk in next_12_hours_data]))

        return '. '.join([
            'Here is the forecast for the day:'
            'Weather should be {}'.format(', '.join(weather_types)),
            'Temperatures should be between {} and {} degrees celsius'.format(min_temp, max_temp)
        ])
