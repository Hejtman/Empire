import time
import logging
from datetime import datetime, timedelta

from spider import Spider

WAIT_BETWEEN_JUMPS = 6
CHECK_BEFORE_ARRIVAL = 30


class Plan:
    def __init__(self, spider, priority, queue):
        self._spider = spider

        self.next_event_date = datetime.now()
        self.priority = priority
        self._queue = queue
        self._queue.reverse()


class Voyage(Plan):
    def __init__(self, spider, name, fleet, voyage, home):
        Plan.__init__(self, spider, priority=1, queue=voyage)

        self.name = name
        self.fleet = fleet
        self.home = home
        self.traveling_to = None
        self.arrival_date = None

    def execute_next_step(self):
        # FIXME: caught exceptions here > fallback
        if self.traveling_to:
            self.check_destination()
            self.next_event_date = self.arrival_date + timedelta(seconds=WAIT_BETWEEN_JUMPS)
        elif self._queue:
            self.traveling_to = self._queue.pop()
            self.arrival_date = self.jump(self.traveling_to)
            self.next_event_date = self.arrival_date - timedelta(seconds=CHECK_BEFORE_ARRIVAL)
        else:
            logging.info(self.name + ' finished.')

    def jump(self, destination):
        logging.debug('{} jumping to {}'.format(self.name, destination))
        travel_time = self._spider.move_fleet(self.fleet, destination)
        arrival_date = Spider.arrival_date(travel_time)
        logging.info('{} jumped to {} travel {} arrive {} jumps {}'
                     .format(self.name, destination, travel_time, str(arrival_date), len(self._queue)))
        return arrival_date

    def check_destination(self):
        # TODO: fleets = self.spider.astro_fleets(self.traveling_to)
        # TODO: self.priority = fleet size (* 1000 if enemy in last sniff)
        self.traveling_to = None  # no more landing checks, next_event is another jump
        logging.debug('{} checked'.format(self.name))
        return datetime.now() - timedelta(seconds=3)  # FIXME

    def fallback(self):
        # TODO: recall? + move home
        pass


if __name__ == "__main__":
    import sys
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)-15s %(message)s')

    sniffer = Voyage(Spider(), 'sniffer',
                     fleet='http://jade.astroempires.com/fleet.aspx?fleet=730480',
                     voyage=['http://jade.astroempires.com/map.aspx?loc=J14:54:16:31',
                             'http://jade.astroempires.com/map.aspx?loc=J14:54:16:20',
                             'http://jade.astroempires.com/map.aspx?loc=J14:54:16:10'],
                     home='http://jade.astroempires.com/base.aspx?base=5451')

    for i in range(100):
        sniffer.execute_next_step()
        wait = (sniffer.next_event_date - datetime.now()).total_seconds()
        if wait > 0:
            logging.info('waiting {}s'.format(wait))
            time.sleep(wait)
