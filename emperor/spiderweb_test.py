import sys
import logging

from location import Location
from spiderweb import SpiderWeb


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)-15s %(message)s')


if __name__ == "__main__":

    print(type(SpiderWeb.arrival_date('0:00:00')))
    print(SpiderWeb.arrival_date('0:00:01'))
    print(SpiderWeb.arrival_date('0:01:00'))
    print(SpiderWeb.arrival_date('1:00:00'))
    print(SpiderWeb.arrival_date('24:00:00'))
    print(SpiderWeb.arrival_date('48:00:00'))

    sp = SpiderWeb()

    for l, d in sp.sniff_system(Location('http://jade.astroempires.com/map.aspx?loc=J14:43:95')):
        print(l.full())
        print(d)
    """
    duration = sp.move_fleet(fleet='http://jade.astroempires.com/fleet.aspx?fleet=730480',
                             destination=Location('http://jade.astroempires.com/map.aspx?loc=J14:54:16:20'))
    
    arrive = Spider.arrival_date(duration)
    print('arrive: ' + str(arrive))

    print(sp.sniff_system(Location('http://jade.astroempires.com/map.aspx?loc=J05:69:55')))
    print(sp.astro_fleets(Location('http://jade.astroempires.com/map.aspx?loc=J05:69:55:10')))
    sp.get_page('http://jade.astroempires.com/base.aspx?base=21886')
    sp.update_cache('J05:69:55:10_base')
    print(list(sp.map_galaxy_systems('http://jade.astroempires.com/map.aspx?loc=J14')))

    report = sp.sniff_system('http://jade.astroempires.com/map.aspx?loc=J14:55:79')
    for ast in report.items():
        print(ast)

    print(sp.get_systems("http://jade.astroempires.com/map.aspx?loc=J14:20"))

    sp.get_page('http://jade.astroempires.com/base.aspx?base=21886')
    print(sp.sniff_player('http://jade.astroempires.com/profile.aspx?player=1309'))
    print(sp.sniff_player('http://jade.astroempires.com/profile.aspx?player=464'))
    
    print(str(len(sp.sniff_system(Location('http://jade.astroempires.com/map.aspx?loc=J14:44:65')))))
    """