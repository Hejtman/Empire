from location import Location
from database import Database


class GalaxyScoutPlanner:
    def __init__(self, db, start):
        self.db = db
        self.not_visited_regions = [int(r) for r in db.get_data(start.galaxy()).keys()]
        self.start = start
        self.direction = 0

    @staticmethod
    def clusterize(data):
        x = 0
        y = 0
        for s in data.keys():
            x += int(int(s) / 10)
            y += int(s) % 10
        return str(round(x/len(data))) + str(round(y/len(data)))

    def non_visited_neighbour_regions(self, region):
        region_int = int(region)
        return (Location(self.start.galaxy(), region_int=region_int + x) for x in [1, -1, 10, -10]
                if region_int + x in self.not_visited_regions)

    def next_region(self, location, regions):
        choice = None
        choice_value = 9999
        for region in regions:
            destination_loc = self.db.get_nearest_astro(location, (region,))
            location_clusterized = Location(location=location.region(),
                                            system=self.clusterize(self.db.get_data(location.region())), astro="00")
            destination_density = len(self.db.get_data(destination_loc.region()))
            destination_continue = len(list(self.non_visited_neighbour_regions(str(destination_loc.region())[-2:])))
            destination_value = location_clusterized.distance(destination_loc) / destination_density**0.5
            if destination_continue and choice_value > destination_value:
                choice = destination_loc
                choice_value = destination_value
        return choice

    def plan(self):
        path = []
        destination = self.start
        while destination:
            path.append(destination)
            current_region = str(destination.region())[-2:]
            self.not_visited_regions.remove(int(current_region))
            next_region_options = self.non_visited_neighbour_regions(current_region)
            destination = self.next_region(destination, next_region_options)

        print(100 * len(self.not_visited_regions) / (len(path) + len(self.not_visited_regions)))

        while self.not_visited_regions:
            loc_i = self.not_visited_regions.pop()
            choice_i = 0
            choice_loc = None
            choice_value = 99999

            for i, l in enumerate(path):
                for x in [-1, 1, -10, 10]:
                    if loc_i + x == l.region_int():
                        location = self.db.get_nearest_astro(l, (Location(self.start.galaxy(), region_int=loc_i),))
                        value = location.distance(l)
                        if choice_value > value:
                            choice_i = i
                            choice_loc = location
                            choice_value = value
            if choice_loc:
                path.insert(choice_i, choice_loc)

        return path


database = Database(None)
database._database_file += '_test.db'
with database:
    planner = GalaxyScoutPlanner(database, start=Location('http://jade.astroempires.com/map.aspx?loc=J10:87:87:11'))
    p = planner.plan()
    for loc in p:
        print("                            Location('{}'),".format(loc.full()))

