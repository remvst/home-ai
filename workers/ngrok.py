import logging
import subprocess
import threading
from time import sleep

import config
from bot.kik_bot import bot
from utils.ngrok import run_ngrok, get_ngrok_url

def worker():
    thread = threading.Thread(target=notify_ngrok_worker)
    thread.start()

    run_ngrok(port=config.KIK_BOT_PORT)


def notify_ngrok_worker():
    while True:
        sleep(2) # Wait a little bit just so ngrok can start

        try:
            ngrok_url = get_ngrok_url()
        except Exception as e:
            logging.exception(e)
            continue

        break

    bot.update_config(webhook=ngrok_url)
