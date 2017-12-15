import logging
from governors.fleet import Fleet
from location import Location


class Probe(Fleet):
    """
    Probe operates in tree modes according what is has in the queue:
     1) Watch = hiding in given region (prefer inactive player bases, empty systems)
     2) Voyage = sniffing given regions (prefer empty systems)
     3) Examine = visit given astros (e.g.: base)
    """
    def __init__(self, spiderweb, database, name, fleet, voyage, sniff_region=False):
        Fleet.__init__(self, spiderweb, database, name, fleet, priority=1, queue=voyage)
        self.sniff_region = sniff_region

    def step(self):
        if self._queue:
            self.sniff()
            self.move()
        else:
            self.stay_hidden()

    def sniff(self):
        if not self.location:
            return

        if self.database.get_data(self.location).base:
            logging.info("{} sniffing base at {}".format(self.name, self.location.full()))
            self._spiderweb.sniff_base(self.location)

        if self.sniff_region:
            logging.info("{} sniffing region {}".format(self.name, self.location.region()))
            self.sniff_all_systems_within_region(self.location.region())

        # TODO: scout closely interesting targets + report

    def move(self):
        if self._queue:
            destination = self._queue.pop()
            if not destination.is_astro():
                destination = self.find_hiding_place(destination.region())
            self.jump(destination)

    def sniff_all_systems_within_region(self, region):
        for system_loc in self.database.get_data(region).keys():
            system_full_loc = Location(region.full() + ":" + system_loc)
            for astro_full_loc, astro_data in self._spiderweb.sniff_system(system_full_loc):
                self.database.set_astro(astro_full_loc, astro_data)
