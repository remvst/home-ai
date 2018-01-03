import logging
from datetime import time
from time import sleep

from helpers.alarm_clock import AlarmClock, AlarmClockSetting
from scripts.good_morning import generate_string
from workers.speech import add_to_queue
from scripts.good_morning import generate_string as good_morning
from utils.clapclap import wait_for_clap_clap

def worker():
    while True:
        wait_for_clap_clap()

        # We got a clap, do something
        string = good_morning()
        add_to_queue(string)
