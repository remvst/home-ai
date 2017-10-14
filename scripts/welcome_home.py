import config
from plugins.google_calendar_summarizer import GoogleCalendarSummarizer, get_credentials
from plugins.news_summarizer import NewsSummarizer
from plugins.time_announcer import TimeAnnouncer


google_calendar_summarizer = GoogleCalendarSummarizer(credentials=get_credentials(
    client_secrets_file='oauth_secret2.json',
    application_name='Home AI Google Calendar access'
))

news_summarizer = NewsSummarizer(
    api_key=config.NEWS_API_KEY,
    sources=['bbc-news']
)

time_announcer = TimeAnnouncer()

def generate_string():
    lines = [
        'Welcome home Remi',
        time_announcer.generate_string(),
        google_calendar_summarizer.generate_string(),
        news_summarizer.generate_string()
    ]
    return '.'.join(lines)
