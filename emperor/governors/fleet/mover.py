import logging
from governors.fleet import Fleet


class Mover(Fleet):
    def __init__(self, spiderweb, database, name, fleet, voyage):
        Fleet.__init__(self, spiderweb, database, name, fleet, priority=1, queue=voyage)

    def step(self):
        self.move()

    def move(self):
        if self._queue:
            destination = self._queue.pop()
            if not destination.is_astro():
                destination = self.find_hiding_place(destination.region())
            self.jump(destination)
        elif self.enemy_fleet_in_system():
            self.jump(destination=self.find_hiding_place(self.location.region()))
