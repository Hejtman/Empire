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
                        fleet = Location('http://jade.astroempires.com/fleet.aspx?fleet=877663'),
                        voyage=[
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:87:87:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:67:99:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:68:92:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:78:03:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:77:74:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:76:59:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:86:09:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:84:29:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:85:18:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:75:98:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:74:29:21'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:73:29:20'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:63:99:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:72:29:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:62:69:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:53:60:20'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:52:96:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:42:94:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:43:00:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:44:00:20'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:45:31:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:55:16:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:54:89:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:64:19:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:65:06:20'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:66:02:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:57:80:21'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:56:91:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:46:91:20'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:36:83:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:35:79:30'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:24:99:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:34:59:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:33:09:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:02:89:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:12:07:30'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:13:72:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:23:53:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:22:39:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:21:39:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:32:10:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:31:08:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:41:12:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:30:87:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:40:18:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:50:06:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:51:40:31'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:03:77:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:04:73:30'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:14:79:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:15:99:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:25:29:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:26:78:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:27:91:31'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:37:87:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:47:59:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:48:98:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:58:18:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:05:99:30'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:06:86:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:16:28:21'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:17:59:23'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:18:71:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:28:97:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:38:77:41'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:39:90:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:49:41:11'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:59:10:20'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:60:09:10'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:61:30:21'),
#                            Location('http://jade.astroempires.com/map.aspx?loc=J10:71:11:20'),
                            Location('http://jade.astroempires.com/map.aspx?loc=J10:81:08:10'),
                            Location('http://jade.astroempires.com/map.aspx?loc=J10:82:23:11'),
                            Location('http://jade.astroempires.com/map.aspx?loc=J10:92:15:10'),
                            Location('http://jade.astroempires.com/map.aspx?loc=J10:93:00:10'),
                            Location('http://jade.astroempires.com/map.aspx?loc=J10:94:20:10'),
                            Location('http://jade.astroempires.com/map.aspx?loc=J10:96:34:11'),
                            Location('http://jade.astroempires.com/map.aspx?loc=J10:95:53:11'),
                        ])

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
