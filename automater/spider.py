import time
import datetime
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config import SERVER, EMAIL, PASSWORD


WAIT = 0.2
WAIT_FOR_PAGE_LOAD = 1


class Spider:
    """
    Wraps the whole web interaction. Parsing, taping, etc.
    """
    def __init__(self):
        self.__browser = webdriver.Firefox()

    def __del__(self):
        logging.info('Logging out.')
        self.__browser.close()

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
            time.sleep(WAIT)

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
        
        :param astro: 'http://jade.astroempires.com/map.aspx?loc=J14:54:16:40'
        :return: ((Fleet, Player, Arrival, Size),)
        """
        self.get_page(astro)
        fleets = self.__browser.find_element_by_xpath('//div[@id="map_fleets"]')
        t = tuple(t.text for t in fleets.find_elements_by_xpath('.//td'))
        return zip(t[::4], t[1::4], t[2::4], t[3::4])

    def move_fleet(self, fleet, destination, wait=1, attempts=10):
        """Move fleet to coordinates.
        
        :param fleet: 'http://jade.astroempires.com/fleet.aspx?fleet=730480'
        :param destination:  'http://jade.astroempires.com/map.aspx?loc=J14:54:16:40'
        :param wait: how many second wait between attempts
        :param attempts: how many times try to move the fleet
        
        :return: travel duration
        :raise ValueError
        """
        page = '{}&view=move&destination={}'.format(fleet, destination.split("loc=", 1)[1])
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

        logging.debug('Fleet travels to {} for {}'.format(destination, travel_duration))
        return travel_duration

    def recall_fleet(self, fleet):
        self.get_page(fleet)
        self.__browser.find_element_by_xpath('//input[@name="confirm_cb"]').click()
        self.__browser.find_element_by_xpath('//input[@value="Recall Fleet"]').click()

    def sniff_system(self, system):
        """Check the system and return interesting stuff
        
        :param system: 'http://jade.astroempires.com/map.aspx?loc=J05:76:35'
        :return: [['astro', [fleets], debris],]
        """
        self.get_page(system)

        reports = []

        system = self.__browser.find_element_by_xpath('//div[@id="map-system_content"]')
        for a in system.find_elements_by_xpath('.//div[contains(@id, "astro_icons_")]'):
            if a.text:
                attributes = a.get_attribute("innerHTML")
                astro_id = a.get_attribute("id").split('astro_icons_')[1]
                astro = '{}/map.aspx?loc={}'.format(SERVER, astro_id)
                enemy_fleet = 'Fleet' in attributes and 'color: Yellow' in attributes
                debris = int(attributes.split(' Debris')[0].split('title="')[-1]) if ' Debris' in attributes else 0
                reports.append([astro, enemy_fleet, debris])

        for i, report in enumerate(reports):
            astro = report[0]
            enemy_fleet = report[1]
            reports[i][1] = self.astro_fleets(astro) if enemy_fleet else ()

        return reports

    def pillage(self, base):
        self.get_page(base + '&action=pillage')

    def _get_element(self, xpath, wait, page=None, reload_max=0):
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
    def arrival_date(travel_time):
        h, m, s = travel_time.split(':')
        dt = datetime.timedelta(seconds=int(s), minutes=int(m), hours=int(h))
        return datetime.datetime.now() + dt


if __name__ == "__main__":
    import sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)-15s %(message)s')

    print(Spider.arrival_date('0:00:00'))
    print(Spider.arrival_date('0:00:01'))
    print(Spider.arrival_date('0:01:00'))
    print(Spider.arrival_date('1:00:00'))
    print(Spider.arrival_date('24:00:00'))
    print(Spider.arrival_date('48:00:00'))

    sp = Spider()
    duration = sp.move_fleet(fleet='http://jade.astroempires.com/fleet.aspx?fleet=730480',
                             destination='http://jade.astroempires.com/map.aspx?loc=J14:54:16:20')

    arrive = Spider.arrival_date(duration)
    print('arrive: ' + str(arrive))
