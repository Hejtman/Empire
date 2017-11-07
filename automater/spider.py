import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from config import SERVER, EMAIL, PASSWORD


WAIT = 0.2
WAIT_LONG = 1


class Spider:
    def __init__(self):
        self.browser = webdriver.Firefox()

    def __del__(self):
        self.browser.close()

    def __login(self):
        self.browser.find_element_by_xpath('//input[@name="email"]').send_keys(EMAIL)
        self.browser.find_element_by_xpath('//input[@name="pass"]').send_keys(PASSWORD)
        self.browser.find_element_by_xpath('//input[@value="Login"]').click()

    def get_page(self, page):
        """Set browser to given page (log-in if needed) and make sure browser is on that page.
        :param page: e.g: 'http://jade.astroempires.com/map.aspx?loc=J14:54:16:40' 
        """
        self.browser.get(page)

        if self.browser.title == 'Login':
            self.__login()
            time.sleep(WAIT)

        if self.browser.current_url != page:
            raise ValueError('Requested page {}, but got: '.format(page, self.browser.current_url))

    def parse_notifications(self):
        """ 
        :return: ((Date, Description),)
        """
        self.get_page(SERVER + '/notifications.aspx')
        t = tuple(t.text for t in self.browser.find_elements_by_xpath('//td'))
        return zip(t[::2], t[1::2])

    def astro_fleets(self, astro):
        """Return tuple of fleets on astro.
        
        :param astro: 'http://jade.astroempires.com/map.aspx?loc=J14:54:16:40'
        :return: ((Fleet, Player, Arrival, Size),)
        """
        self.get_page(astro)
        fleets = self.browser.find_element_by_xpath('//div[@id="map_fleets"]')
        t = tuple(t.text for t in fleets.find_elements_by_xpath('.//td'))
        return zip(t[::4], t[1::4], t[2::4], t[3::4])

    def move_fleet(self, fleet, destination):
        """Move fleet to coordinates.
        
        :param fleet: 'http://jade.astroempires.com/fleet.aspx?fleet=730480'
        :param destination:  'http://jade.astroempires.com/map.aspx?loc=J14:54:16:40'
        
        :return: arrival time
        Rise ValueError or AttributeError exception otherwise.
        """
        self.get_page(fleet + '&view=move')

        destination_coordinates = destination.split("loc=", 1)[1]
        destination_input = self.browser.find_element_by_xpath('//input[@id="destination"]')
        fleet_name = self.browser.find_element_by_xpath('//option[@selected="selected"]')
        fleet_name = fleet_name.text.split(' - ')[0].strip()

        destination_input.send_keys(Keys.BACKSPACE*12)
        destination_input.send_keys(destination_coordinates)
        destination_input.send_keys(Keys.ENTER)

        time.sleep(WAIT_LONG)
        fleets = self.browser.find_element_by_xpath('//div[@id="fleets-list"]')
        t = tuple(t.text for t in fleets.find_elements_by_xpath('.//td'))
        for f_name, f_arrival in zip(t[::6], t[3::6]):
            if f_name == fleet_name:
                return f_arrival.split(' @ ')[1]
        raise ValueError('Fleet is not moving?')

    def recall_fleet(self, fleet):
        self.get_page(fleet)
        self.browser.find_element_by_xpath('//input[@name="confirm_cb"]').click()
        self.browser.find_element_by_xpath('//input[@value="Recall Fleet"]').click()

    def sniff_system(self, system):
        """Check the system and return interesting stuff
        
        :param system: 'http://jade.astroempires.com/map.aspx?loc=J05:76:35'
        :return: [['astro', [fleets], debris],]
        """
        self.get_page(system)

        reports = []

        system = self.browser.find_element_by_xpath('//div[@id="map-system_content"]')
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


if __name__ == "__main__":
    spider = Spider()
    print(spider.sniff_system('http://jade.astroempires.com/map.aspx?loc=J05:76:35'))
