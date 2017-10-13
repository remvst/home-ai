from datetime import datetime, timedelta

from lib.utils import is_user_in_network

DEFAULT_AWAY_THRESHOLD=timedelta(minutes=10)

class HomeCheck(object):

    def __init__(self, mac_addresses, away_threshold=DEFAULT_AWAY_THRESHOLD):
        super(HomeCheck, self).__init__()

        self.mac_addresses = mac_addresses
        self.away_threshold = away_threshold

        self.is_home = None
        self.last_time_in_network = datetime.now()

        self.came_home_handler = None
        self.left_home_handler = None

    def check(self):
        is_home = any(is_user_in_network(addr) for addr in self.mac_addresses)

        if self.is_home is None:
            self.is_home = is_home
            return

        if is_home:
            self.last_time_in_network = datetime.now()
            self.maybe_welcome()
        else:
            self.maybe_goodbye()

    def maybe_welcome(self):
        if self.is_home:
            return # Already home

        self.is_home = True

        if self.came_home_handler is not None:
            self.came_home_handler.run()

    def maybe_goodbye(self):
        if not self.is_home:
            return # Already considered gone

        away_time = datetime.now() - self.last_time_in_network
        if away_time < self.away_threshold:
            return # Not away for long enough

        # Okay now he's gone for sure
        self.is_home = False

        if self.left_home_handler is not None:
            self.left_home_handler.run()
