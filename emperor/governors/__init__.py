from datetime import datetime


class Governor:
    def __init__(self, spiderweb, database, priority, queue):

        self.spiderweb = spiderweb
        self.database = database
        self.priority = priority
        self._queue = queue
        self._queue.reverse()
        self.next_event_date = datetime.now()
