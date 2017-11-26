import logging
from governors.fleet import Fleet


class Probe(Fleet):
    """
    Probe operates in tree modes according what is has in the queue:
     1) Watch = hiding in given region (prefer inactive player bases, empty systems)
     2) Voyage = sniffing given regions (prefer empty systems)
     3) Examine = visit given astros (e.g.: base)
    """
    def __init__(self, spiderweb, database, name, fleet, voyage):
        Fleet.__init__(self, spiderweb, database, name, fleet, priority=1, queue=voyage)

    def step(self):
        if self.location:
            self.sniff()
        self.move()

    def sniff(self):
        current_location_info = self.database.get_data(self.location)

        if current_location_info and current_location_info.base:
            logging.info("{} sniffing base at {}".format(self.name, self.location.full()))
            self.spiderweb.sniff_base(self.location)
        else:
            region = self.location.region()
            logging.info("{} sniffing region {}".format(self.name, region.full()))
            self.sniff_all_systems_within_region(region)

    def move(self):
        if self._queue:
            destination = self._queue.pop()
            if not destination.is_astro():
                destination = self.find_hiding_place(destination.region())
            self.jump(destination)
        elif self.enemy_fleet_in_system():
            self.jump(destination=self.find_hiding_place(self.location.region()))

    def sniff_all_systems_within_region(self, region):
        for s in tuple(self.database.get_systems(region)):
            for astro, report in self.spiderweb.sniff_system(s):
                self.database.update_astro(astro, report)
