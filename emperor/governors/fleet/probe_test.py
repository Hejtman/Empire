import sys
import time
import logging
from datetime import datetime

from database import Database
from governors.fleet.probe import Probe
from location import Location
from spiderweb import SpiderWeb
from utils import seconds_to_string


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)-15s %(message)s')


if __name__ == "__main__":
    sp = SpiderWeb()
    db = Database(sp)
    db._database_file += '_test.db'
    with db:
        sniffer = Probe(spiderweb=sp, database=db, name='voyager15', sniff_region=True,
                        fleet = Location('http://jade.astroempires.com/fleet.aspx?fleet=841332'),
                        voyage=[
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:87:96:11'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:96:34:11'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:95:45:21'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:94:49:21'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:93:34:41'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:92:39:41'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:82:95:11'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:81:37:21'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:71:75:41'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:70:19:41'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:60:99:11'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:61:80:11'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:51:80:21'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:50:59:21'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:41:91:21'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:40:49:21'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:30:97:31'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:31:80:11'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:21:99:21'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:22:81:21'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:23:50:41'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:13:99:31'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:14:90:11'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:24:18:21'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:25:05:31'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:15:97:11'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:26:01:11'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:27:80:10'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:37:05:21'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:47:97:41'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:57:70:11'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:67:03:11'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:66:19:21'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:56:91:11'),
#                             Location('http://jade.astroempires.com/map.aspx?loc=J15:55:99:41'),
                             Location('http://jade.astroempires.com/map.aspx?loc=J15:65:00:21'),
                        ])
        """
                         voyage=[Location('http://jade.astroempires.com/map.aspx?loc=J15:61:30:20'),
                                 Location('http://jade.astroempires.com/map.aspx?loc=J15:60:39:31'),
                                 Location('http://jade.astroempires.com/map.aspx?loc=J15:60:39:31'),
                                 Location('http://jade.astroempires.com/map.aspx?loc=J15:60:39:31'),
                                 Location('http://jade.astroempires.com/map.aspx?loc=J15:50:59:21'),
                                 Location('http://jade.astroempires.com/map.aspx?loc=J15:51:31:21'),
                                 Location('http://jade.astroempires.com/map.aspx?loc=J15:41:40:11'),
                                 Location('http://jade.astroempires.com/map.aspx?loc=J15:40:49:21'),
                                 Location('http://jade.astroempires.com/map.aspx?loc=J15:30:67:21'),
                                 Location('http://jade.astroempires.com/map.aspx?loc=J15:31:30:21'),
                                 Location('http://jade.astroempires.com/map.aspx?loc=J15:21:85:21')]
                        )

        sniffer = Probe(spiderweb=sp, database=db, name='voyager14', sniff_region=True,
                        fleet=Location('http://jade.astroempires.com/fleet.aspx?fleet=840297'),
                        voyage=[Location('http://jade.astroempires.com/map.aspx?loc=J14:43'),
                                Location('http://jade.astroempires.com/map.aspx?loc=J14:44'),
                                Location('http://jade.astroempires.com/map.aspx?loc=J14:45'),
                                Location('http://jade.astroempires.com/map.aspx?loc=J14:55'),
                                Location('http://jade.astroempires.com/map.aspx?loc=J14:54'),
                                Location('http://jade.astroempires.com/map.aspx?loc=J14:53'),
                                Location('http://jade.astroempires.com/map.aspx?loc=J14:54:16:40')]
                        )
        """
#        sniffer.sniff_all_systems_within_region(Location('http://jade.astroempires.com/map.aspx?loc=J14:43'))

        for i in range(10000):
            if sniffer.next_event_date > datetime.now():
                wait = (sniffer.next_event_date - datetime.now()).total_seconds()
                logging.debug('{} into next action'.format(seconds_to_string(wait)))
                time.sleep(min(wait, 20))
            else:
                sniffer.execute_step()


# find hiding place should rely on database more?

# move to region
# move to astro
# move to base empty
# move to base with enemy
