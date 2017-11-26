import pickle
import logging
from contextlib import suppress

from config import DATABASE
from location import Location


class Database:
    def __init__(self, _spiderweb):
        self._database_file = DATABASE
        self._spiderweb = _spiderweb
        self._players = {}
        self._locations = {}

    def __enter__(self):
        with suppress(FileNotFoundError):
            self._load()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._save()

    def get_data(self, location):
        node = self._locations
        loc = str(location)[1:].split(':')

        galaxy = loc[0]
        try:
            self._locations[galaxy]
        except KeyError:
            logging.debug('Accessed galaxy data were not found! Mapping whole galaxy: ' + galaxy)
            self.__map_galaxy(location.galaxy())

        for l in loc:
            node = node[l]
        return node

    def set_astro(self, location, data):
        # todo: diff day, week
        node = self._locations
        loc = str(location)[1:].split(':')

        galaxy = loc[0]
        astro = loc.pop()
        try:
            self._locations[galaxy]
        except KeyError:
            logging.debug('Accessed galaxy data were not found! Mapping whole galaxy: ' + galaxy)
            self.__map_galaxy(location.galaxy())

        for l in loc:
            node = node[l]
        node[astro] = data

    def get_first_astros_with_empty_system(self, region):
        for system_loc, system_node in self.get_data(region).items():
            if all(a_data.fleets_neutral + a_data.fleets_enemy == 0 for a_loc, a_data in system_node.items()):
                yield Location("{}:{}:{}".format(region.full(), system_loc, iter(system_node.keys()).__next__()))

    def player_info(self, player):
        try:
            return self._players[player]
        except KeyError:
            return self.update_player_info(player)

    def update_player_info(self, player):
        logging.debug('Updating player {} info.'.format(player))
        self._players[player] = self._spiderweb.sniff_player(player)
        return self._players[player]

    def get_free_inactive_players_bases(self, region):
        for system_loc, system_node in self.get_data(region).items():
            for astro_loc, astro_data in system_node.items():
                if astro_data.base and not astro_data.occ and self.player_info(astro_data.owner).inactive:
                    yield Location("{}:{}:{}".format(region.full(), system_loc, astro_loc))

    def _load(self):
        with open(self._database_file, 'rb') as f:
            logging.debug('loading database')
            self._players = pickle.load(f)
            self._locations = pickle.load(f)

    def _save(self):
        with open(self._database_file, 'wb') as f:
            logging.debug('saving database')
            pickle.dump(self._players, f, pickle.HIGHEST_PROTOCOL)
            pickle.dump(self._locations, f, pickle.HIGHEST_PROTOCOL)

    def __map_galaxy(self, galaxy):
        for system in self._spiderweb.parse_galaxy_systems(galaxy):
            node = self._locations
            for loc in str(system)[1:].split(':'):
                try:
                    node = node[loc]
                except KeyError:
                    node[loc] = node = {}
