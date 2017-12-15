import time
import logging
from datetime import datetime, timedelta

from governors import Governor


WAIT_AFTER_ARRIVAL = 1
WAIT_BETWEEN_JUMPS = timedelta(seconds=6)
MINIMUM_CHECKING_PERIOD = 3*60
CHECKING_PERIOD = 12*60


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
        travel_time = self._spiderweb.move_fleet(self.fleet, destination)
        self.arrival_date = self._spiderweb.arrival_date(travel_time)
        logging.info('{} jumped to {} travel {} arrive {} jumps {}'
                     .format(self.name, destination.full(), travel_time, str(self.arrival_date), len(self._queue)))
        self.location = destination
        self.next_event_date = self.arrival_date + timedelta(seconds=WAIT_AFTER_ARRIVAL)

    def stay_hidden(self):
        if self.enemy_fleet_in_system():
            self.jump(destination=self.find_hiding_place(self.location.region()))
        else:
            self.wait(MINIMUM_CHECKING_PERIOD + CHECKING_PERIOD/self.priority)

    def wait(self, seconds):
        self.next_event_date = datetime.now() + timedelta(seconds)

    def find_hiding_place(self, region):
        # FIXME: allay bases first (JG)
        try:
            loc = self.database.get_free_inactive_players_bases(region).__next__()
            logging.debug('Found hiding place at inactive base: {}'.format(loc.full()))
        except StopIteration:
            try:
                loc = self.database.get_first_astros_with_empty_system(region).__next__()
                logging.debug('Found hiding place {} at empty system.'.format(loc.full()))
            except StopIteration:
                loc = self.database.get_any_astro(region).__next__()
                logging.debug('Found place: {}'.format(loc.full()))
        return loc

    def enemy_fleet_in_system(self):
        system_report = self._spiderweb.sniff_system(self.location.system())
        return any(r.fleet_neutral or r.fleet_enemy for loc, r in system_report)
