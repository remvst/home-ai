import httplib2
import json
import os
from datetime import date, datetime, time, timedelta
from dateutil import parser

from apiclient import discovery

from lib.text_plugin import TextPlugin

class GoogleCalendarSummarizer(TextPlugin):

    def __init__(self, credentials):
        super(GoogleCalendarSummarizer, self).__init__()
        self.credentials = credentials

    def fetch_events(self):
        http = self.credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        today = date.today()
        tomorrow = today + timedelta(days=1)

        today_start = datetime.combine(today, time())
        tomorrow_start = datetime.combine(tomorrow, time())

        events_result = service.events().list(
            calendarId='primary',
            timeMin=today_start.isoformat() + 'Z',
            timeMax=tomorrow_start.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        return events_result.get('items', [])

    def generate(self):
        try:
            events = self.fetch_events()
        except:
            return 'Error getting Google Calendar events'

        if len(events) == 0:
            return 'you have no events scheduled for today'

        lines = ['you have {} event{} scheduled today'.format(len(events), 's' if len(events) > 1 else '')]

        for event in events:
            event_name = event['summary']
            event_time = parser.parse(event['start']['dateTime'])
            event_time_format = event_time.strftime('%I:%M%p')

            line = '{}, at {}'.format(event_name, event_time_format)
            lines.append(line)

        return '. '.join(lines)
