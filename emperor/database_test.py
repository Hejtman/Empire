from datetime import datetime

from location import Location
from database import Database
from spiderweb import AstroData, PlayerData
from spiderweb_fake import SpiderWeb
from spiderweb import SpiderWeb as SpiderWebReal


def that_it_maps_galaxy_when_get_data():
    # given
    sp = SpiderWeb()
    sp.parse_galaxy_systems_ret = (Location('http://jade.astroempires.com/map.aspx?loc=J01:00:01'),
                                   Location('http://jade.astroempires.com/map.aspx?loc=J01:00:02'),
                                   Location('http://jade.astroempires.com/map.aspx?loc=J02:00:00'))
    astro1_loc = '01'
    astro1_data = ('astro 1 data 1', 'data 2')
    astro2_loc = '02'
    astro2_data = ('astro 2 data 1', 'data 2')
    astro3_loc = '01'
    astro3_data = ('data 1', 'data 2')
    sp.sniff_system_ret[Location('http://jade.astroempires.com/map.aspx?loc=J01:00:01')] = ((astro1_loc, astro1_data),
                                                                                            (astro2_loc, astro2_data))
    sp.sniff_system_ret[Location('http://jade.astroempires.com/map.aspx?loc=J01:00:02')] = ()
    sp.sniff_system_ret[Location('http://jade.astroempires.com/map.aspx?loc=J02:00:00')] = ((astro3_loc, astro3_data),)
    db = Database(sp)
    db._database_file += '_test.db'

    # when
    data1 = db.get_data(Location('http://jade.astroempires.com/map.aspx?loc=J01:00'))
    data2 = db.get_data(Location('http://jade.astroempires.com/map.aspx?loc=J02:00'))

    # then
    assert data1 == {'01': {astro1_loc: astro1_data, astro2_loc: astro2_data}}
    assert data2 == {'00': {astro3_loc: astro3_data}}
    assert db._locations == {'01': {'00': {'01': {astro1_loc: astro1_data, astro2_loc: astro2_data}}},
                             '02': {'00': {'00': {astro3_loc: astro3_data}}}}


def that_it_maps_galaxy_when_set_data():
    # given
    sp = SpiderWeb()
    sp.parse_galaxy_systems_ret = (Location('http://jade.astroempires.com/map.aspx?loc=J01:00:01'),
                                   Location('http://jade.astroempires.com/map.aspx?loc=J01:00:02'),
                                   Location('http://jade.astroempires.com/map.aspx?loc=J02:00:00'))
    db = Database(sp)
    db._database_file += '_test.db'
    now = datetime.now()

    # when
    db.set_astro(Location('http://jade.astroempires.com/map.aspx?loc=J01:00:01:01'),
                 AstroData(0, 0, 0, 10, 12345, 1234, 4321, 'rocky1', now))
    db.set_astro(Location('http://jade.astroempires.com/map.aspx?loc=J02:00:00:01'),
                 AstroData(0, 0, 0, 10, 12345, 1234, 4321, 'rocky2', now))

    # then
    assert db._locations == {'01': {'00': {'01': {'01': AstroData(0, 0, 0, 10, 12345, 1234, 4321, 'rocky1', now)},
                                           '02': {}}},
                             '02': {'00': {'00': {'01': AstroData(0, 0, 0, 10, 12345, 1234, 4321, 'rocky2', now)}}}}


def that_it_gives_free_inactive_players_bases():
    # given
    now = datetime.now()
    sp = SpiderWeb()

    db = Database(sp)
    db._locations = {'08': {'04': {'01': {'01': AstroData(0, 0, 0, 10, None, None, None, 'empty', now)},
                                   '02': {},
                                   '03': {'01': AstroData(0, 0, 0, 10, 17, 7, None, 'base', now)},
                                   '04': {'02': AstroData(0, 0, 0, 10, 18, 8, 7, 'occ', now)},
                                   '05': {'01': AstroData(0, 0, 0, 10, 19, 9, 8, 'occ', now)},
                                   '06': {'01': AstroData(0, 0, 0, 10, None, None, None, 'empty', now)}}}}
    db._players = {7: PlayerData('NAME', 'guild', 3.14, 30, True, 18, True, now),
                   8: PlayerData('NAME', 'guild', 3.14, 30, True, 18, True, now),
                   9: PlayerData('NAME', 'guild', 3.14, 30, True, 18, False, now)}

    # when
    inactive_bases = db.get_free_inactive_players_bases(Location('http://jade.astroempires.com/map.aspx?loc=J08:04'))

    # then
    assert inactive_bases.__next__() == Location('http://jade.astroempires.com/map.aspx?loc=J08:04:03:01')


def unit_t_est():
    db = Database(None)
    db._database_file += '_test.db'
    db._locations['00'] = {'00': {'00': {'00': AstroData(0, 0, 0, 10, 12345, 1234, 4321, 'rocky', datetime.now())}}}
    db.set_astro('J00:00:00:01', AstroData(0, 0, 0, 10, 12345, 1234, 4321, 'rocky', datetime.now()))

    assert db._locations['00'] == db.get_data(Location('http://jade.astroempires.com/map.aspx?loc=J00'))
    assert db._locations['00']['00'] == db.get_data(Location('http://jade.astroempires.com/map.aspx?loc=J00:00'))
    assert db._locations['00']['00']['00'] == db.get_data('J00:00:00')
    assert db._locations['00']['00']['00']['00'] == db.get_data('J00:00:00:00')
    assert db._locations['00'] == db.get_data(Location('http://jade.astroempires.com/map.aspx?loc=J00'))

    print(db._locations['00'])
    print(db._locations['00']['00'])
    print(db._locations['00']['00']['00'])
    print(db._locations['00']['00']['00']['00'])
    print(db.get_data(Location('http://jade.astroempires.com/map.aspx?loc=J00:00:00:00')))
    print(db.get_data(Location('http://jade.astroempires.com/map.aspx?loc=J00:00:00:01')))

    that_it_maps_galaxy_when_get_data()
    #  that_it_maps_galaxy_when_set_data()
    #  that_it_gives_free_inactive_players_bases()

    with db:
        for l in db.get_abandoned_derb_piles(Location('http://jade.astroempires.com/map.aspx?loc=J14:44:96:20')):
            print(l)
            print(l.distance('J14:44:96:20'))
            print(db.get_data(l))


if __name__ == "__main__":
    # unit_t_est()

    sp = SpiderWebReal()
    db = Database(sp)
    db._database_file += '_test.db'

    with db:
        for region_loc, region_node in db.get_data(Location('loc=J15')).items():
            for l in db.get_free_inactive_players_bases(Location('loc=J15', region_loc), min_level=25):
                print(l.full())
