import logging
import threading
from time import sleep

def infinite_thread(worker, name):
    def infinite_worker():
        while True:
            try:
                worker()
            except Exception as e:
                logging.error(u'Worker {} crashed'.format(name))
                logging.exception(e)
                sleep(1)
            finally:
                pass

    thread = threading.Thread(target=infinite_worker, name=name)
    thread.daemon = True

    return thread
