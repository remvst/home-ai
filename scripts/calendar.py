from plugins.google_calendar_summarizer import GoogleCalendarSummarizer, get_credentials
from utils.content import TextContent
from utils.script import Script


class CalendarScript(Script):

    def run(self, input_content):
        google_calendar_summarizer = GoogleCalendarSummarizer(credentials=get_credentials(
            client_secrets_file='oauth_secret2.json',
            application_name='Home AI Google Calendar access'
        ))

        self.output([TextContent(google_calendar_summarizer.generate_string())])
