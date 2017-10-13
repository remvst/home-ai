import logging
from datetime import time
from time import sleep

from helpers.alarm_clock import AlarmClock, AlarmClockSetting
from scripts.good_morning import generate_string
from workers.speech import add_to_queue


def ring():
    string = generate_string()
    add_to_queue(string)

alarm_clock = AlarmClock([
    AlarmClockSetting(weekday=0, time=time(hour=10, minute=0)),
    AlarmClockSetting(weekday=1, time=time(hour=10, minute=0)),
    AlarmClockSetting(weekday=2, time=time(hour=10, minute=0)),
    AlarmClockSetting(weekday=3, time=time(hour=10, minute=0)),
    AlarmClockSetting(weekday=4, time=time(hour=10, minute=0)),
    AlarmClockSetting(weekday=5, time=time(hour=10, minute=30)),
    AlarmClockSetting(weekday=6, time=time(hour=10, minute=30))
])
alarm_clock.ring_handler = ring

def worker():
    while True:
        logging.debug('Check alarm clock')
        alarm_clock.check()
        sleep(5)
