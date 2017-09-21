from datetime import datetime, timedelta

from lib.utils import is_user_in_network

DEFAULT_AWAY_THRESHOLD=timedelta(minutes=10)

class HomeCheck(object):

    def __init__(self, mac_addresses, away_threshold=DEFAULT_AWAY_THRESHOLD):
        super(HomeCheck, self).__init__()

        self.mac_addresses = mac_addresses
        self.away_threshold = away_threshold

        self.is_home = False
        self.last_time_home = datetime.now()

        self.came_home_handler = None
        self.left_home_handler = None

    def check(self):
        is_home = any(is_user_in_network(addr) for addr in self.mac_addresses)

        if is_home:
            self.last_time_home = datetime.now()
            if not self.is_home:
                self.is_home = True
                if self.came_home_handler is not None:
                    self.came_home_handler.run()
            return

        away_time = datetime.now() - self.last_time_home
        if away_time > self.away_threshold:
            self.is_home = False
            if self.left_home_handler is not None:
                self.left_home_handler.run()
