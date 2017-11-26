import time
import logging
from datetime import datetime, timedelta

from governors import Governor


WAIT_AFTER_ARRIVAL = 1
WAIT_BETWEEN_JUMPS = timedelta(seconds=6)


class Fleet(Governor):
    def __init__(self, spiderweb, database, name, fleet, priority, queue):
        Governor.__init__(self, spiderweb, database, name, priority, queue)
        self.fleet = fleet
        self.location = None
        self.arrival_date = datetime.now() - WAIT_BETWEEN_JUMPS  # no need to wait for the first jump

    # noinspection PyTypeChecker
    def jump(self, destination):
        soonest_jump_date = self.arrival_date + WAIT_BETWEEN_JUMPS
        if soonest_jump_date > datetime.now():
            wait_for_jump = (soonest_jump_date - datetime.now()).total_seconds()
            logging.debug('Waiting for jump {}s'.format(wait_for_jump))
            assert wait_for_jump < 10, 'Waiting {}s for jump is too long'.format(wait_for_jump)
            time.sleep(wait_for_jump)

        logging.debug('{} jumping to {}'.format(self.name, destination.full()))
        travel_time = self.spiderweb.move_fleet(self.fleet, destination)
        self.arrival_date = self.spiderweb.arrival_date(travel_time)
        logging.info('{} jumped to {} travel {} arrive {} jumps {}'
                     .format(self.name, destination.full(), travel_time, str(self.arrival_date), len(self._queue)))
        self.location = destination
        self.next_event_date = self.arrival_date + timedelta(seconds=WAIT_AFTER_ARRIVAL)

    def find_hiding_place(self, region):
        for base_location in self.database.get_free_inactive_players_bases(region):
            logging.debug('Found hiding place at inactive base: {}'.format(base_location.full()))
            return base_location

        for astro_location in self.database.get_first_astros_with_empty_system(region):
            logging.debug('Found hiding place at empty system: {}'.format(astro_location.full()))
            return astro_location

        raise ValueError('No hiding place was found!')

    def enemy_fleet_in_system(self):
        system_report = self.spiderweb.sniff_system(self.location.system())
        return any(r.fleet_neutral or r.fleet_enemy for loc, r in system_report)

    def fallback(self):
        super().fallback()
        if self._queue:
            self._queue.pop()
