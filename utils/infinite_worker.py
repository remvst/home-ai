import logging
from time import sleep


def infinite_worker(worker):

    def _worker(*args):
        while True:
            try:
                worker(*args)
                return
            except KeyboardInterrupt:
                raise
            except Exception as e:
                logging.exception(e)
                sleep(1)

    return _worker
