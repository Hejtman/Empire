import sys
import time
import logging
from datetime import datetime

from database import Database
from governors.fleet.recycler import Recycler
from location import Location
from spiderweb import SpiderWeb
from utils import seconds_to_string


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)-15s %(message)s')


if __name__ == "__main__":
    sp = SpiderWeb()
    db = Database(sp)
    db._database_file += '_test.db'
    with db:
        rec1 = Recycler(spiderweb=sp, database=db, name='rec1',
                        fleet=Location('http://jade.astroempires.com/fleet.aspx?fleet=840301'),
                        voyage=[Location('http://jade.astroempires.com/map.aspx?loc=J14:43')]
                        )

