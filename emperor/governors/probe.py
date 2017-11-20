import time
import logging
from datetime import datetime, timedelta
from utils import is_astro, location_to_system, location_to_region

from spiderweb import SpiderWeb
from database import Database
from governors import Governor


WAIT_AFTER_ARRIVAL = 1
WAIT_BETWEEN_JUMPS = timedelta(seconds=6)


class Probe(Governor):
    """
    Probe operates in tree modes according what is has in the queue:
     1) Watch = hiding in given region (prefer inactive player bases, empty systems)
     2) Voyage = sniffing given regions (prefer empty systems)
     3) Examine = visit given astros (e.g.: base)
    """
    def __init__(self, spiderweb, database, name, fleet, voyage):
        Governor.__init__(self, spiderweb, database, priority=1, queue=voyage)

        self.name = name
        self.fleet = fleet
        self.fails = 0
        self.location = 'http://jade.astroempires.com/map.aspx?loc=J14:43:17'  # None
        self.arrival_date = datetime.now() - WAIT_BETWEEN_JUMPS  # ready for jump immediately

    def execute_next_step(self):
        try:
#            if self.location:
#                self.sniff()
            self.move()

        except AssertionError:  #(IndexError, ValueError, AttributeError):
            self.fallback()

    def sniff(self):
        current_location_info = self.database.astro.get(self.location)

        if current_location_info and current_location_info.base:
            logging.info("{} sniffing base at {}".format(self.name, self.location))
            self.spiderweb.sniff_base(self.location)
        else:
            region = location_to_region(self.location)
            logging.info("{} sniffing region {}".format(self.name, region))
            self.sniff_all_systems_within_region(region)

    def move(self):
        if not self._queue:
            self.stay_hidden()
        else:
            next_destination = self._queue.pop()
            if is_astro(next_destination):
                self.jump(next_destination)
            else:
                self.jump(destination=self.find_hiding_place(next_destination))

    def stay_hidden(self):
        system_report = self.spiderweb.sniff_system(location_to_system(self.location))
        print(system_report)
        if any(r.neutral_fleet_present or r.neutral_fleet_incoming for loc, r in system_report):
            self.jump(destination=self.find_hiding_place(self.location))

    # noinspection PyTypeChecker
    def jump(self, destination):
        soonest_jump_date = self.arrival_date + WAIT_BETWEEN_JUMPS
        if soonest_jump_date > datetime.now():
            wait_for_jump = (soonest_jump_date - datetime.now()).total_seconds()
            logging.debug('Waiting for jump {}s'.format(wait_for_jump))
            time.sleep(wait_for_jump)

        logging.debug('{} jumping to {}'.format(self.name, destination))
        travel_time = self.spiderweb.move_fleet(self.fleet, destination)
        self.arrival_date = SpiderWeb.arrival_date(travel_time)
        logging.info('{} jumped to {} travel {} arrive {} jumps {}'
                     .format(self.name, destination, travel_time, str(self.arrival_date), len(self._queue)))
        self.location = destination
        self.next_event_date = self.arrival_date + timedelta(seconds=WAIT_AFTER_ARRIVAL)

    def fallback(self):
        self.next_event_date = datetime.now() + timedelta(minutes=self.fails ** 4)  # 0, 1, 16min, 1h, 4h
        self.fails += 1
        logging.error('{} execution failed {}! Next attempt at {}'.format(self.name, self.fails, self.next_event_date))
        # TODO: alert if fails > 3

    def find_hiding_place(self, destination):

        print(self.database.astro.items())
        region = location_to_region(destination)
        for location, astro in self.database.astro.items():  #todo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            print(location)
            if region in location and astro.base:
                print(location)
                if self.database.player['http://jade.astroempires.com/profile.aspx?player=' + astro.owner].inactive:
                    return location

#        for s in self.database.get_systems(self.spiderweb, region):
#        region = location_to_region(destination)
#        for s in self.database.get_systems(self.spiderweb, region):
#            if not any(r.neutral_fleet_present or r.neutral_fleet_incoming or r.base for r in s.report):
#                return s

    def sniff_all_systems_within_region(self, region):
        for s in self.database.get_systems(self.spiderweb, region):
            for astro, report in self.spiderweb.sniff_system(s):
                self.database.update_astro(astro, report)


if __name__ == "__main__":
    import sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)-15s %(message)s')

    spw = SpiderWeb()
    db = Database()
    with db:
        sniffer = Probe(spiderweb=spw, database=db, name='voyager14',
                        fleet='http://jade.astroempires.com/fleet.aspx?fleet=730480',
                        voyage=[]#'http://jade.astroempires.com/map.aspx?loc=J14:54:16:31']
                        )
        for i in range(1):  # 10
            if sniffer.next_event_date > datetime.now():
                wait = (sniffer.next_event_date - datetime.now()).total_seconds()
                logging.info('waiting {}s'.format(wait))
                time.sleep(wait)
            sniffer.execute_next_step()