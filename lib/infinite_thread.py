import threading
import traceback

class InfiniteThread(threading.Thread):

    def __init__(self, target, crash_handler, *args, **kwargs):
        super(InfiniteThread, self).__init__(target=self.target_wrapper(target), *args, **kwargs)

        self.crash_handler = crash_handler

    def target_wrapper(self, target):
        def wrapper():
            while True:
                try:
                    target()
                except Exception as e:
                    logging.exception(e)
                    self.crash_handler(exception=e, description=traceback.format_exc())
                    sleep(10)  # Give it a bit of time before restarting
                else:
                    return  # Thread finished successfully, we can stop looping

        return wrapper
