import time
import logging
from datetime import datetime, timedelta

from spiderweb import SpiderWeb
from database import Database
from governors import Governor


WAIT_AFTER_ARRIVAL = 6
WAIT_BETWEEN_JUMPS = 6
CHECK_BEFORE_ARRIVAL = 30

# FIXME: probe is supposed to sit in final destination and watch (support checking destination within region)
# No checks before arrival
# Fall back to nearest inhabited sector within region and stay there


class Probe(Governor):
    def __init__(self, name, fleet, voyage, home):
        Governor.__init__(self, priority=1, queue=voyage)

        self.name = name
        self.fleet = fleet
        self.home = home
        self.destination = None
        self.arrival_date = None
        self.fails = 0

    def execute_next_step(self, spiderweb, database):
        try:
            if self.arrival_date > datetime.now():
                self.check_destination(spiderweb)
                self.next_event_date = self.arrival_date + timedelta(seconds=WAIT_AFTER_ARRIVAL)
            else:
                Probe.probe_region(spiderweb=spiderweb, database=database, region=self.destination[-6:0])
                self.arrival_date = self.jump(spiderweb, destination=self._queue.pop())  # FIXME: just iterator
                self.next_event_date = self.arrival_date - timedelta(seconds=CHECK_BEFORE_ARRIVAL)
        except (IndexError, ValueError):
            if self.destination == self.home:
                self.next_event_date = None
                logging.info(self.name + ' finished.')
                return

            self.next_event_date = datetime.now() + timedelta(minutes=self.fails ** 4)  # 0, 1, 16min, 1h, 4h, 10h
            self.fails += 1
            if not self._queue:
                self._queue = (self.home,)
            logging.error('{} execution failed {}! Next target {}.'.format(self.name, self.fails, self._queue[-1]))

    def jump(self, spiderweb, destination):
        logging.debug('{} jumping to {}'.format(self.name, destination))
        travel_time = spiderweb.move_fleet(self.fleet, destination)
        arrival_date = SpiderWeb.arrival_date(travel_time)
        logging.info('{} jumped to {} travel {} arrive {} jumps {}'
                     .format(self.name, destination, travel_time, str(arrival_date), len(self._queue)))
        self.destination = destination
        return arrival_date

    def check_destination(self, spiderweb):
        logging.debug('{} checking {} before arrival.'.format(self.name, self.destination))
        destination_system = self.destination[:-3]
        destination_system_report = spiderweb.sniff_system(destination_system)

        destination_report = destination_system_report[self.destination]
        if destination_report.neutral_fleet_present or destination_report.neutral_fleet_incoming:
            logging.warning('Avoiding fleet at: {} {}<{}'.format(self.destination,
                                                                 destination_report.neutral_fleet_present,
                                                                 destination_report.neutral_fleet_incoming))
            self.next_event_date = spiderweb.recall_fleet(self.fleet)
            # TODO: add next_system within region to the queue (top?bottom)
            return

        self.priority = sum(r.neutral_fleet_present + r.neutral_fleet_incoming for r in destination_system_report)
        logging.debug('{} checked'.format(self.name))

    @staticmethod
    def probe_region(spiderweb, database, region):
        try:
            systems = database.get_systems(region)
        except KeyError:
            systems = spiderweb.get_systems(region)

        for s in systems:
            for astro, report in spiderweb.sniff_system(s):
                database.astros[astro] = report


if __name__ == "__main__":
    import sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)-15s %(message)s')

    sniffer = Probe('sniffer',
                    fleet='http://jade.astroempires.com/fleet.aspx?fleet=730480',
                    voyage=['http://jade.astroempires.com/map.aspx?loc=J14:54:16:31'],
                    home='http://jade.astroempires.com/base.aspx?base=5451')

    spw = SpiderWeb()
    db = Database()
    for i in range(10):
        sniffer.execute_next_step(spw, db)
        wait = (sniffer.next_event_date - datetime.now()).total_seconds()
        if wait > 0:
            logging.info('waiting {}s'.format(wait))
            time.sleep(wait)
