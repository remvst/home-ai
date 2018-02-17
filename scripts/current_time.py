import config
from plugins.google_calendar_summarizer import GoogleCalendarSummarizer, get_credentials
from plugins.news_summarizer import NewsSummarizer
from plugins.quote_of_the_day import QuoteOfTheDay
from plugins.time_announcer import TimeAnnouncer
from plugins.weather_announcer import WeatherAnnouncer
from utils.content import TextContent
from utils.script import Script


class CurrentTimeScript(Script):

    def run(self, input_content):
        time_announcer = TimeAnnouncer()

        quote_of_the_day = QuoteOfTheDay()

        weather_announcer = WeatherAnnouncer(
            api_key=config.OPEN_WEATHER_MAP_API_KEY,
            location_query='waterloo,ontario'
        )

        lines = [
            'Good morning Remi. Time to wake up',
            time_announcer.generate_string(),
            google_calendar_summarizer.generate_string(),
            news_summarizer.generate_string(),
            weather_announcer.generate_string(),
            quote_of_the_day.generate_string(),
            'Have an amazing day'
        ]

        string = u'.'.join(lines)

        self.output([TextContent(strintime_announcer.generate_string())])
