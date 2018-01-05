import logging
from datetime import time
from time import sleep

from helpers.alarm_clock import AlarmClock, AlarmClockSetting
from scripts.good_morning import generate_string as good_morning
from utils.clapclap import wait_for_clap_clap
from utils.sound import play_mp3
from workers.speech import add_to_queue

def worker():
    logging.debug('sleeeping.....')
    sleep(10)
    logging.debug('done sleeping')

    while True:
        logging.debug('got a clap?')
        wait_for_clap_clap()
        logging.debug('processed!')

        # We got a clap, do something
        play_mp3('assets/clap-detected.mp3')

        string = good_morning()
        add_to_queue(string)
