import config
from plugins.weather_announcer import WeatherAnnouncer
from utils.content import TextContent
from utils.script import Script


class WeatherScript(Script):

    def run(self, input_content):
        weather_announcer = WeatherAnnouncer(
            api_key=config.OPEN_WEATHER_MAP_API_KEY,
            location_query='waterloo,ontario'
        )

        self.output([TextContent(weather_announcer.generate_string())])
