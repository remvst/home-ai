import httplib2
import os
from datetime import date, datetime, time, timedelta
from dateutil import parser
import json

import pytz
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from tzlocal import get_localzone

from plugins.text_plugin import TextPlugin

def get_credentials(client_secrets_file, application_name):
    """
    https://developers.google.com/google-apps/calendar/quickstart/python
    """
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    credential_path = os.path.join(credential_dir, 'home-ai-google-calendar.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secrets_file, SCOPES)
        flow.user_agent = application_name
        credentials = tools.run_flow(flow, store, flags)

    return credentials

class GoogleCalendarSummarizer(TextPlugin):

    def __init__(self, credentials):
        super(GoogleCalendarSummarizer, self).__init__()
        self.credentials = credentials

    def fetch_events(self):
        http = self.credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        today = date.today()
        tomorrow = today + timedelta(days=1)

        local = get_localzone()

        today_start = local.localize(datetime.combine(today, time()))
        tomorrow_start = local.localize(datetime.combine(tomorrow, time()))

        events_result = service.events().list(
            calendarId='primary',
            timeMin=today_start.isoformat(),
            timeMax=tomorrow_start.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        return events_result.get('items', [])

    def generate_string(self):
        try:
            events = self.fetch_events()
        except Exception as e:
            return 'Error getting Google Calendar events: {}'.format(e.message)

        if len(events) == 0:
            return 'You have no events scheduled for today'

        lines = ['You have {} event{} scheduled today'.format(len(events), 's' if len(events) > 1 else '')]

        for event in events:
            event_name = event['summary']

            if 'dateTime' in event['start']:
                event_time = parser.parse(event['start']['dateTime'])
                event_time_format = 'at {}'.format(event_time.strftime('%I:%M%p'))
            else:
                event_time_format = 'the whole day'

            line = '{}, {}'.format(event_name, event_time_format)
            lines.append(line)

        return '. '.join(lines)
