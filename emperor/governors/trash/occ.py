from spiderweb import SpiderWeb
from config import OCCUPATIONS


class Capitan:
    """
    Represents single instance of plan (queue = series of actions on subject[s].
    e.g.: Moving fleet trough several astros, fighter-drop, regular astro sniffing, regular occ pillage, etc.   
    
    Capitan carry the entire plan with all its checks, fall-backs and lets the General only to serialize those topmost 
    actions between capitans/governors/queues according its priorities as via spider only one action at time is possible
    """
    def __init__(self, spider):
        self.spider = spider

    def pillage_bases(self):
        for occ in OCCUPATIONS:
            self.spider.pillage(occ)

    def start_voyage(self, fleet, voyage, priority):
        self.spider.move_fleet()

if __name__ == "__main__":
    s = SpiderWeb()
    capitan = Capitan(s)
    capitan.pillage_bases()

#    capitan.move_fleet('f', ('http://jade.astroempires.com/map.aspx?loc=J05:76', ))
