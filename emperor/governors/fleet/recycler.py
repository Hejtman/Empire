import logging
from governors.fleet import Fleet


class Recycler(Fleet):
    def __init__(self, spiderweb, database, name, fleet, voyage):
        Fleet.__init__(self, spiderweb, database, name, fleet, priority=1, queue=voyage)

    def step(self):
        fleet, debris = self.sniff()
        if fleet or not debris:
            self.move()

    def sniff(self):
        system_report = self._spiderweb.sniff_system(self.location.system())
        has_fleet = any(r.fleet_neutral or r.fleet_enemy for loc, r in system_report)
        debris = 0  # FIXME: debris = system_report[1].debris where system_report[0] == self.location[-2:]
        return has_fleet, debris

    def move(self):
        try:
            self.jump(self._queue.pop())
        except StopIteration:
            self.jump(destination=self.find_hiding_place(self.location.region()))
