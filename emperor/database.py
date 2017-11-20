import pickle
import logging
from contextlib import suppress
from config import DATABASE, MAP_GALAXIES
from location import Location


class Database:
    def __init__(self, spiderweb):
        self.database_file = DATABASE
        self.spiderweb = spiderweb
        self.players = {}
        self.locations = {}

    def __enter__(self):
        with suppress(FileNotFoundError):
            self.load()
            self.map_galaxies()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    def load(self):
        with open(self.database_file, 'rb') as f:
            self.players = pickle.load(f)
            self.locations = pickle.load(f)

    def save(self):
        with open(self.database_file, 'wb') as f:
            pickle.dump(self.players, f, pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.locations, f, pickle.HIGHEST_PROTOCOL)

    def map_galaxies(self):
        for g in MAP_GALAXIES:
            galaxy = Location(g)
            try:
                self.get_systems(galaxy).__next__()
            except StopIteration:
                logging.debug('No system found for galaxy {}. Updating systems in whole galaxy.'.format(galaxy.full()))
                self.locations.update({system: None for system in self.spiderweb.parse_galaxy_systems(galaxy)})

    def get_systems(self, location):
        for system in self.locations.keys():
            if system.is_system() and system in location:
                yield system

    def player_info(self, player):
        try:
            player_info = self.players[player]
        except KeyError:
            player_info = self.update_player(player)
        return player_info

    def update_astro(self, astro, report):
        # TODO: diff
        logging.debug('update_astro({}, {})'.format(astro.full(), report))
        self.locations[astro] = report

    def update_player(self, player):
        # TODO: old names, guilds
        # TODO: diff
        logging.debug('Updating player {} info.'.format(player))
        self.players[player] = self.spiderweb.sniff_player(player)
        return self.players[player]

    def get_inactive_players_bases(self, location):
        for loc, data in self.locations.items():
            if loc.is_astro() and loc in location and data.base and self.player_info(data.owner).inactive:
                yield loc

if __name__ == "__main__":
    import sys
    from datetime import datetime
    from spiderweb import SpiderWeb, AstroData
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)-15s %(message)s')

    sp = SpiderWeb()
    d = Database(sp)
    d.database_file += '_test.db'

    with d:
#        print(sp.sniff_system(Location('http://jade.astroempires.com/map.aspx?loc=J14:81:54')))
        region = Location('http://jade.astroempires.com/map.aspx?loc=J14:63')
#        for system in tuple(d.get_systems(region)):
#            for astro, report in sp.sniff_system(system):
#                d.update_astro(astro, report)

        for l in d.get_inactive_players_bases(region):
            print(l.full())
#        d.update_astro(Location("http://jade.astroempires.com/map.aspx?loc=J05:69:55:10"),
#                       AstroData(neutral_fleet_present=31925, neutral_fleet_incoming=0, debris=0, astro_size='crystalline',
#                                 base='18570', owner='1707', owner_level=32.46, owner_guild='[/M\\]  Grimmjow (DEOS)',
#                                 timestamp=datetime.now()))

#        with suppress(KeyError):
#            print(d.players['test'])
#        d.update_player(None, 'test')

#        for s in d.get_systems(None, Location('http://jade.astroempires.com/map.aspx?loc=J14:81')):
#            print(s.full())

#        for location, data in d.locations.items():
#            print(str(location) + '   ' + str(data))

#        for id, data in d.players.items():
#            print(id + '   ' + data)
