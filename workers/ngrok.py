import logging
from threading import Thread

from kik import Configuration

from utils.ngrok import run_ngrok, get_ngrok_url

def get_worker(port, kik):

    def worker():
        while True:
            thread = Thread(target=notify_ngrok_worker)
            thread.start()

            try:
                run_ngrok(port=port)
            except:
                pass


    def notify_ngrok_worker():
        while True:
            try:
                ngrok_url = get_ngrok_url()
                break
            except Exception as e:
                continue

        logging.debug('ngrok available at {}'.format(ngrok_url))

        kik.set_configuration(Configuration(webhook=ngrok_url))

    return Thread(target=worker, name='ngrok')
