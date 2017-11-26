import sys
import time
import logging
from datetime import datetime

from location import Location
from spiderweb import SpiderWeb
from database import Database
from governors.probe import Probe


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)-15s %(message)s')


if __name__ == "__main__":
    sp = SpiderWeb()
    db = Database(sp)
    db._database_file += '_test.db'
    with db:
        sniffer = Probe(spiderweb=sp, database=db, name='voyager14',
                        fleet=Location('http://jade.astroempires.com/fleet.aspx?fleet=730480'),
                        voyage=[Location('http://jade.astroempires.com/map.aspx?loc=J14:43'),
                                Location('http://jade.astroempires.com/map.aspx?loc=J14:44'),
                                Location('http://jade.astroempires.com/map.aspx?loc=J14:45'),
                                Location('http://jade.astroempires.com/map.aspx?loc=J14:55'),
                                Location('http://jade.astroempires.com/map.aspx?loc=J14:54'),
                                Location('http://jade.astroempires.com/map.aspx?loc=J14:53'),
                                Location('http://jade.astroempires.com/map.aspx?loc=J14:54:16:40')]
                        )

#        sniffer.sniff_all_systems_within_region(Location('http://jade.astroempires.com/map.aspx?loc=J14:43'))

        for i in range(100):
            if sniffer.next_event_date > datetime.now():
                wait = (sniffer.next_event_date - datetime.now()).total_seconds()
                logging.debug('{}s into next action'.format(wait))
                time.sleep(min(wait, 20))
            else:
                sniffer.execute_step()


# find hiding place should rely on database more?

# move to region
# move to astro
# move to base empty
# move to base with enemy
