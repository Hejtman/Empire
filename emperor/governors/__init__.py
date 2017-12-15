import logging
from datetime import datetime, timedelta


class Governor:
    def __init__(self, spiderweb, database, name, priority, queue):

        self._spiderweb = spiderweb
        self.database = database
        self.name = name
        self.priority = priority
        self._queue = queue
        self._queue.reverse()
        self.next_event_date = datetime.now()
        self.fails = 0

    def execute_step(self):
        try:
            self.step()

        except (ValueError, StopIteration):  # (IndexError, AttributeError, AssertionError):
            logging.exception("Error in {} execute_step".format(self.name))
            self.fallback()

    def step(self):
        assert False, 'This should be re-defined in child.'  # FIXME: python pure virtual function?

    def fallback(self):
        self.next_event_date = datetime.now() + timedelta(minutes=self.fails ** 4)  # 0, 1, 16min, 1h, 4h
        self.fails += 1
        logging.error('{} execution failed {}! Next attempt at {}'.format(self.name, self.fails, self.next_event_date))
        # TODO: alert if fails > 3
