import logging
from datetime import time
from time import sleep

from helpers.alarm_clock import AlarmClock, AlarmClockSetting
from utils.content import Content


def get_worker(response):
    alarm_clock = AlarmClock([
        AlarmClockSetting(weekday=0, time=time(hour=9, minute=0)),
        AlarmClockSetting(weekday=1, time=time(hour=9, minute=0)),
        AlarmClockSetting(weekday=2, time=time(hour=9, minute=0)),
        AlarmClockSetting(weekday=3, time=time(hour=9, minute=0)),
        AlarmClockSetting(weekday=4, time=time(hour=9, minute=0)),
        AlarmClockSetting(weekday=5, time=time(hour=10, minute=30)),
        AlarmClockSetting(weekday=6, time=time(hour=10, minute=30))
    ])

    def worker():
        while True:
            if not alarm_clock.check():
                sleep(5)
                continue

            response.maybe_handle(Content())

    return worker
