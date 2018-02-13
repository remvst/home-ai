from collections import deque
from datetime import date, datetime, time


class AlarmClockSetting(object):

    def __init__(self, weekday, time):
        super(AlarmClockSetting, self).__init__()
        self.weekday = weekday
        self.time = time


class AlarmClock(object):

    def __init__(self, settings):
        super(AlarmClock, self).__init__()

        self.settings = deque(settings)

        now = datetime.now()
        current_day_of_week = now.weekday()

        for i in xrange(len(self.settings)):
            if self.settings[0].weekday == current_day_of_week:
                break

            # keep rotating
            self.rotate()

        # Skip past settings of the day (to avoid ringing right away)
        for i in xrange(len(self.settings)):
            if self.settings[0].weekday != current_day_of_week:
                break

            if datetime.combine(date.today(), self.settings[0].time) > now:
                break

            self.rotate()

    def rotate(self):
        self.settings.rotate(-1)

    def check(self):
        current_setting = self.settings[0]

        now = datetime.now()
        current_day_of_week = now.weekday()

        if current_day_of_week != current_setting.weekday:
            return False

        ring_time = datetime.combine(date.today(), current_setting.time)

        if now < ring_time:
            return False

        self.rotate()

        return True
