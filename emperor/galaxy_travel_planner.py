from location import Location
from database import Database


db = Database(None)
db._database_file += '_test.db'


beginning = Location('http://jade.astroempires.com/map.aspx?loc=J15:96:46:10')
path = []


def nearest_astro(location, regions):
    nearest = None
    for region in regions:
        region_node = db.get_data(region)
        for system_loc, system_node in region_node.items():
            for astro_loc, astro_data in system_node.items():
                loc = Location(location=region, system=system_loc, astro=astro_loc)
                if not nearest or location.distance(nearest) > location.distance(loc):
                    nearest = loc
    return nearest


def next_region(location, regions, not_visited_regions, recursion=0):
    choice = None
    choice_value = None
    for region in regions:
        destination = nearest_astro(location, (region,))
        back = nearest_astro(destination, (location.region(),))
        destination_value = location.distance(destination) + destination.distance(back)

        # 22 > 32 > 33!
        destination_continue = list(non_visited_neighbour_regions(int(str(destination.region())[-2:]),
                                                                  not_visited_regions))
        if not choice_value or destination_continue and choice_value > destination_value:
            choice = destination
            choice_value = destination_value
            if recursion:
                next_next_options = list(non_visited_neighbour_regions(int(str(destination.region())[-2:]),
                                                                  not_visited_regions))
                _, next_choice_value = next_region(destination, next_next_options, not_visited_regions, recursion=recursion-1)
                if next_choice_value:
                    choice_value += next_choice_value/len(next_next_options)
                else:
                    choice_value += 200

    return choice, choice_value


def non_visited_neighbour_regions(region_int, not_visited_regions):
    return (Location(beginning.galaxy(), region_int=region_int + x) for x in [1, -1, 10, -10]
            if region_int + x in not_visited_regions)


with db:
    not_visited_regions = [int(r) for r in db.get_data(beginning.galaxy()).keys()]
    destination = beginning
    while destination:
        path.append(destination)
        current_region = int(str(destination.region())[-2:])
        not_visited_regions.remove(current_region)
        next_region_options = non_visited_neighbour_regions(current_region, not_visited_regions)
        destination, _ = next_region(destination, next_region_options, not_visited_regions)

    # TODO: deal with the not_visited_regions


for p in path:
    print(p.full())

print(not_visited_regions)
print(100*len(not_visited_regions)/(len(path)+len(not_visited_regions)))

# find closest planet to current location



#for system_loc, system_node in region_node.items():
#    for astro_loc, astro_data in system_node.items():
#        if astro_data.debris and not (
#                        astro_data.fleet_allay or astro_data.fleet_neutral or astro_data.fleet_enemy):
#            debris.append(Location(location.galaxy(), region_loc, system_loc, astro_loc))
#return sorted(debris, key=lambda x: x.distance(location))
