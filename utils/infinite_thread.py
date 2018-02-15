import logging
from threading import Thread
from time import sleep

def infinite_thread(worker, name, args=()):

    def infinite_worker(*args):
        while True:
            try:
                worker(*args)
            except KeyboardInterrupt:
                return
            except Exception as e:
                logging.error(u'Worker {} crashed'.format(name))
                logging.exception(e)
                sleep(1)
            finally:
                pass

    return Thread(target=infinite_worker, name=name, args=args)
