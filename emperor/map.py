from database import Database
from location import Location


db = Database(None)
db._database_file += '_test.db'


with db:
    for region_loc, region_node in db.get_data(Location('http://jade.astroempires.com/map.aspx?loc=J14')).items():
        print(region_loc)
        for system_loc, system_node in region_node.items():
           for astro_loc, astro_data in system_node.items():
               print(astro_data)
               a = astro_data._replace(fleet_neutral=0)
               print(a)
               loc = Location('http://jade.astroempires.com/map.aspx?loc=J14:' +
                              str(region_loc) + ":" + str(system_loc) + ":" + str(astro_loc))
               db.set_astro(loc, a)
               print(astro_loc)
               print(loc.full())


                # TODO print interesting planets (Metal +3, Solar or Gas >=4)
                # TODO print enemy fleets per region/sector
                # TODO print bases with JG >= 4

#                print(astro_loc)
#                print(str(astro_loc)[-2:])
#            db.set_astro(self, astro_loc, astro_data):
