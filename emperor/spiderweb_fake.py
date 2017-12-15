import sys
import logging
from datetime import datetime, timedelta
from collections import namedtuple

Astro = namedtuple('Astro', 'neutral_fleet_present neutral_fleet_incoming debris astro_size '
                   + 'base owner owner_level owner_guild probed')

WAIT = 0.2
WAIT_FOR_PAGE_LOAD = 1


class SpiderWeb:
    """
    Wraps the whole web interaction. Parsing, taping, etc.
    """

    def __init__(self):
        self.parse_notifications_ret = ()
        self.astro_fleets_ret = ()
        self.move_fleet_ret = ""
        self.recall_fleet_ret = ""
        self.parse_galaxy_systems_ret = ()
        self.get_systems_ret = ()
        self.sniff_base_ret = ""
        self.sniff_system_ret = {}

    def __del__(self):
        logging.info('Logging out.')

    def get_page(self, page):
        logging.debug("{}({})".format(sys._getframe().f_code.co_name, page))

    def parse_notifications(self):
        logging.debug("{}".format(sys._getframe().f_code.co_name))
        return self.parse_notifications_ret

    def astro_fleets(self, astro):
        logging.debug("{}({})".format(sys._getframe().f_code.co_name, astro))
        return self.astro_fleets_ret

    def move_fleet(self, fleet, destination, wait=1, attempts=10):
        logging.debug("{}({}, {}, {}, {})".format(sys._getframe().f_code.co_name, fleet, destination, wait, attempts))
        return self.move_fleet_ret

    def recall_fleet(self, fleet):
        logging.debug("{}({})".format(sys._getframe().f_code.co_name, fleet))
        return self.recall_fleet_ret

    def parse_galaxy_systems(self, galaxy):
        logging.debug("{}({})".format(sys._getframe().f_code.co_name, galaxy))
        return self.parse_galaxy_systems_ret

    def get_systems(self, region):
        logging.debug("{}({})".format(sys._getframe().f_code.co_name, region))
        return self.get_systems_ret

    def sniff_base(self, astro):
        logging.debug("{}({})".format(sys._getframe().f_code.co_name, astro))
        return self.sniff_base_ret

    def sniff_system(self, system):
        logging.debug("{}({})".format(sys._getframe().f_code.co_name, system))
        return self.sniff_system_ret[system]

    def update_cache(self, file):
        logging.debug("{}({})".format(sys._getframe().f_code.co_name, file))

    def pillage(self, base):
        logging.debug("{}({})".format(sys._getframe().f_code.co_name, base))

    @staticmethod
    def arrival_date(travel_time):
        h, m, s = travel_time.split(':')
        return datetime.now() + timedelta(seconds=int(s), minutes=int(m), hours=int(h))
