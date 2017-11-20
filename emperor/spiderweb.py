import os
import time
import logging
from datetime import datetime, timedelta
from collections import namedtuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config import SERVER, EMAIL, PASSWORD, CACHE_DIR
from location import Location

AstroData = namedtuple('AstroData', 'neutral_fleet_present neutral_fleet_incoming debris astro_size '
                       + 'base owner owner_level owner_guild timestamp')
PlayerData = namedtuple('PlayerData', 'name guild level eco upgraded age inactive timestamp')

WAIT = 0.2
WAIT_FOR_PAGE_LOAD = 1


class SpiderWeb:
    """
    Wraps the whole web interaction. Parsing, taping, etc.
    """
    def __init__(self):
        self.__browser = webdriver.Firefox()

    def __del__(self):
        logging.info('Logging out.')
        self.__browser.close()  # FIXME: persistant connection?

    def __login(self):
        logging.info('Logging in.')
        self.__browser.find_element_by_xpath('//input[@name="email"]').send_keys(EMAIL)
        self.__browser.find_element_by_xpath('//input[@name="pass"]').send_keys(PASSWORD)
        self.__browser.find_element_by_xpath('//input[@value="Login"]').click()

    def get_page(self, page):
        """Set browser to given page (log-in if needed) and make sure browser is on that page.
        :param page: e.g: 'http://jade.astroempires.com/map.aspx?loc=J14:54:16:40' 
        """
        self.__browser.get(page)

        if self.__browser.title == 'Login':
            self.__login()
            time.sleep(WAIT_FOR_PAGE_LOAD)

        if self.__browser.current_url != page:
            raise ValueError('Requested page {}, but got: '.format(page, self.__browser.current_url))

    def parse_notifications(self):
        """ 
        :return: ((Date, Description),)
        """
        self.get_page(SERVER + '/notifications.aspx')
        t = tuple(t.text for t in self.__browser.find_elements_by_xpath('//td'))
        return zip(t[::2], t[1::2])

    def astro_fleets(self, astro):
        """Return tuple of fleets on astro.
        
        :param astro: Location('http://jade.astroempires.com/map.aspx?loc=J14:54:16:40')
        :return: ((Fleet, Player, Arrival, Size),)
        """
        self.get_page(astro.full())
        self.update_cache(str(astro))

        fleets = self.__browser.find_element_by_xpath('//div[@id="map_fleets"]')
        t = tuple(t.text for t in fleets.find_elements_by_xpath('.//td'))
        return zip(t[::4], t[1::4], t[2::4], t[3::4])

    def move_fleet(self, fleet, destination, wait=1, attempts=10):
        """Move fleet to coordinates.
        
        :param fleet: 'http://jade.astroempires.com/fleet.aspx?fleet=730480'
        :param destination:  Location('http://jade.astroempires.com/map.aspx?loc=J14:54:16:40')
        :param wait: how many second wait between attempts
        :param attempts: how many times try to move the fleet
        
        :return: travel duration
        :raise ValueError
        """
        page = '{}&view=move&destination={}'.format(fleet, destination)
        move_xpath = '/html/body/div[1]/div/div/div[2]/div[4]/div/div[2]/div[2]/form/center/input'
        logging.debug('Moving fleet: {}'.format(page))

        for attempt in range(attempts):
            self.get_page(page)
            try:
                self.__browser.find_element_by_xpath(move_xpath).click()
                self.get_page(page)
                travel_duration = self.__browser.find_element_by_xpath('//*[@id="timer1"]').text
                break
            except NoSuchElementException:
                logging.debug('Failed {}/{} attempt to move the fleet!'.format(1+attempt, attempts))
                time.sleep(wait)
        else:
            raise ValueError('Moving fleet failed!')

        logging.debug('Fleet travels to {} for {}'.format(destination.full(), travel_duration))
        return travel_duration

    def recall_fleet(self, fleet):
        self.get_page(fleet)
        self.__browser.find_element_by_xpath('//input[@name="confirm_cb"]').click()
        self.__browser.find_element_by_xpath('//input[@value="Recall Fleet"]').click()
        # TODO: return arrival time

    def parse_galaxy_systems(self, galaxy):
        """
        :param galaxy: Location('http://jade.astroempires.com/map.aspx?loc=J00')
        :return: tuple of all galaxy (solar) systems
        """
        self.get_page(galaxy.full())
        g_map = self.__browser.find_element_by_xpath('//*[@id="map2_ObjTiles0"]')
        system_elements = g_map.find_elements_by_xpath('.//a[contains(@id, "{}:")]'.format(galaxy))
        return (Location("{}/map.aspx?loc={}".format(SERVER, s.get_attribute("id"))) for s in system_elements)

    def sniff_base(self, astro):
        # TODO
        pass

    def sniff_system(self, system):  # FIXME generator
        """Check the system and return interesting stuff
        
        :param system: Location('http://jade.astroempires.com/map.aspx?loc=J05:76:35')
        :return: (('location', Astro()), ...)
        """
        self.get_page(system.full())
        self.update_cache(str(system))

        reports = []
        now = datetime.now()
        system_elm = self.__browser.find_element_by_xpath('//div[@id="map-system_content"]')
        for a in system_elm.find_elements_by_xpath('.//div[contains(@class,"astro_container")]'):
            attributes = a.get_attribute("innerHTML")
            logging.debug('sniff_system - parsing astro: {}'.format(attributes))
            loc = self.__parse_string_between(attributes, 'astro_icons_', '"')
            if not loc:
                loc = self.__parse_string_between(attributes, 'id="astro_', '"')

            if loc:
                location = Location(loc)
                debris_boundary_a = '<small><div style="color: Gray; height: 9px;" title="'
                base_prefix = 'base.aspx?base='
                owner_prefix = 'profile.aspx?player='
                base_id = self.__parse_string_between(attributes, base_prefix, '"')
                owner_id = self.__parse_string_between(attributes, owner_prefix, '"')
                neutral_fleet = self.__parse_string_between(attributes, '"Neutral: Fleet present: ', '">')
                astro_report = (location, AstroData(
                    neutral_fleet_present=int(neutral_fleet.split(' - ')[0]) if neutral_fleet else 0,
                    neutral_fleet_incoming=int(neutral_fleet.split('Incoming: ')[1]) if neutral_fleet else 0,
                    debris=self.__parse_number_between(attributes, debris_boundary_a, ' Debris', 0),
                    astro_size=self.__parse_string_between(attributes, 'class="astro astro_', '">'),
                    base="{}/{}{}".format(SERVER, base_prefix, base_id) if base_id else None,
                    owner="{}/{}{}".format(SERVER, owner_prefix, owner_id) if owner_id else None,
                    owner_level=self.__parse_number_between(attributes, 'Player level ', ' ', 0.0) if owner_id else 0.0,
                    owner_guild=self.__parse_string_between(attributes, 'style="white-space: nowrap;">', '</a>'),
                    # TODO: occ J14:81:76:10
                    timestamp=now
                ))
                logging.debug(astro_report)
                reports.append(astro_report)
        logging.debug(reports)
        return reports

    def sniff_player(self, player):
        self.get_page(player)
        self.update_cache(player.split('player=')[1])
        logging.debug('sniffing player: {}'.format(player))

        attributes = self.__browser.find_element_by_xpath('//*[@id="profile"]').get_attribute("innerHTML")
        logging.debug('attributes: {}'.format(attributes))
        return PlayerData(
            name=self.__parse_string_between(attributes, '<div class="sbox_ctr"><span>', '</span></div><div class="sb'),
            guild=self.__parse_number_between(attributes, 'guild=', '">', 0),
            level=self.__parse_number_between(attributes, 'Level:</b> ', ' (Rank ', 0.0),
            eco=self.__parse_number_between(attributes, 'Economy:</b> ', '<br><br><b>Account:', 0),
            upgraded='title="Upgraded"' in attributes,
            age=self.__parse_number_between(attributes, 'Account Age:</b> ', ' Days', 0),
            inactive='Player Inactive' in attributes,
            timestamp=datetime.now()
        )

    def update_cache(self, file):
        """
        :param file: where to store information 
        """
        save_file = os.path.join(CACHE_DIR, file)
        with open(save_file + '.html', "w") as f:
            f.write(self.__browser.page_source)

    def pillage(self, base):
        self.get_page(base + '&action=pillage')

    def _get_element(self, xpath, parent=None):
        if not parent:
            parent = self.__browser

        try:
            return parent.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return None

    def _get_element2(self, xpath, wait, page=None, reload_max=0):
        """
        Try to locate an UI element on current page and will reload the page if needed.
        
        :param page: e.g.: 'http://jade.astroempires.com/fleet.aspx?fleet=730480&view=move&destination=J14:54:16:31'
        :param xpath: e.g.: '/html/body/div[1]/div/div/div[2]/div[4]/div/div[2]/div[2]/form/center/input'
        :param wait: how many second wait for loading page with element
        :param reload_max: how many times try to reload the page when element was not found on it
         
        :return: WebDriverElement
        :raise ValueError
        """
        reloaded = 0
        while True:
            try:
                element = WebDriverWait(self.__browser, wait).until(ec.presence_of_element_located((By.XPATH, xpath)))
                logging.debug('Element {} found.'.format(xpath))
                return element
            except TimeoutException:
                logging.debug("{}/{} Element {} was not found on {}."
                              .format(reloaded, reload_max, xpath, self.__browser.current_url))
                if reloaded >= reload_max:
                    break

                reloaded += 1
                AssertionError(page)
                self.get_page(page)

        logging.warning("Failed to find an element {} on page {}".format(xpath, self.__browser.current_url))
        raise ValueError("Element not found!")

    def _wait_for_page(self, page, wait):
        for i in range(wait):
            if page == self.__browser.current_url:
                logging.debug('Page {} loaded.'.format(page))
                break
            else:
                logging.debug('{}/{}s still waiting for page: {}'.format(i, wait, page))
                time.sleep(1)
        else:
            logging.warning("{}s and have page {} instead of {}".format(wait, self.__browser.current_url, page))
            raise ValueError("Page was not loaded!")

    @staticmethod
    def __parse_string_between(s, a, b):
        try:
            return s.split(a)[1].split(b)[0]
        except IndexError:
            return None

    @staticmethod
    def __parse_number_between(s, a, b, default_value):
        t = type(default_value)
        string = SpiderWeb.__parse_string_between(s, a, b)
        return t(string) if string else default_value

    @staticmethod
    def arrival_date(travel_time):
        h, m, s = travel_time.split(':')
        return datetime.now() + timedelta(seconds=int(s), minutes=int(m), hours=int(h))


if __name__ == "__main__":
    import sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)-15s %(message)s')

    print(type(SpiderWeb.arrival_date('0:00:00')))
    print(SpiderWeb.arrival_date('0:00:01'))
    print(SpiderWeb.arrival_date('0:01:00'))
    print(SpiderWeb.arrival_date('1:00:00'))
    print(SpiderWeb.arrival_date('24:00:00'))
    print(SpiderWeb.arrival_date('48:00:00'))

    sp = SpiderWeb()
    """
    duration = sp.move_fleet(fleet='http://jade.astroempires.com/fleet.aspx?fleet=730480',
                             destination='http://jade.astroempires.com/map.aspx?loc=J14:54:16:20')

    arrive = Spider.arrival_date(duration)
    print('arrive: ' + str(arrive))

    print(sp.sniff_system('http://jade.astroempires.com/map.aspx?loc=J05:69:55'))
    print(sp.astro_fleets('http://jade.astroempires.com/map.aspx?loc=J05:69:55:10'))
    sp.get_page('http://jade.astroempires.com/base.aspx?base=21886')
    sp.update_cache('J05:69:55:10_base')
    print(list(sp.map_galaxy_systems('http://jade.astroempires.com/map.aspx?loc=J14')))

    report = sp.sniff_system('http://jade.astroempires.com/map.aspx?loc=J14:55:79')
    for ast in report.items():
        print(ast)

    print(sp.get_systems("http://jade.astroempires.com/map.aspx?loc=J14:20"))
    """

    sp.get_page('http://jade.astroempires.com/base.aspx?base=21886')
    print(sp.sniff_player('http://jade.astroempires.com/profile.aspx?player=1309'))
    print(sp.sniff_player('http://jade.astroempires.com/profile.aspx?player=464'))
