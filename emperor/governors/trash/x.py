import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler

from spiderweb import SpiderWeb


class General:
    """
    His responsibility is to serialize ongoing operations as web browser control can have only one capitan at the time.
    e.g.: It is better to miss some debris or wait with base pillage than lose fleet to an enemy attack.
    """
    def __init__(self, spider):
        self.spider = spider
        self.scheduler = BackgroundScheduler({
            'apscheduler.executors.default':
                {'class': 'apscheduler.executors.pool:ThreadPoolExecutor', 'max_workers': '1'}
            }
        )

    def start(self):
        logging.info('Starting scheduler.')
        self.scheduler.start()

    def stop(self):
        logging.info('Stopping scheduler.')
        self.scheduler.shutdown()

    def add_capitan(self, capitan):
        self.scheduler.add_job(capitan, trigger='date', misfire_grace_time=60*60)


def a():
    print("A")


def b():
    print("B")
    time.sleep(1)


if __name__ == "__main__":
    s = SpiderWeb()
    g = General(s)

    g.add_capitan(a)
    g.add_capitan(b)

    g.start()

    time.sleep(10)
    g.stop()
'''
#cron_params = {'trigger': 'cron', 'misfire_grace_time': MISFIRE_GRACE_TIME}
#self.scheduler.add_job(self.garden.watering, trigger='date')
#self.scheduler.add_job(self.garden.watering, minute='*/20', id='WATERING', **cron_params)

    def fighter_drop(self, fleet, target):
        # TODO
        # home = origin
        # move_fleet(fleet, target)
        # if target changed > recall
        # f = split_fleet(all but fighters, home)
        # attack
        # return for survivors
        # move away (recs?)
        pass

    def gather_fleet(self):
        # TODO
        pass

    def patrol_fleet(self):
        # TODO
        pass

    def harvest(self, astro):
        # TODO
        # home = origin
        # t = calculate arrival time
        # f = split_fleet(all but recs, astro)
        # if enemy > recall
        # wait for 30
        # eat all derbs
        # move home
        pass

    def defender(self):
        # TODO
        # for all bases
        # * hunt down scouts in whole sector
        # * think about attacking smaller fleets in home systems
        pass

'''