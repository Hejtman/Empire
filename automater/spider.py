import time
from selenium import webdriver

from config import EMAIL, PASSWORD


WAIT = 0.2


class Spider:
    def __init__(self):
        self.browser = webdriver.Firefox()

    def __del__(self):
        self.browser.close()

    def check_page_login_if_needed(self, page):
        if self.browser.title == 'Login':
            self.login()
            time.sleep(WAIT)

        if page not in self.browser.title:
            raise ValueError('?' + x + '?')

    def login(self):
        email = self.browser.find_element_by_xpath('//input[@name="email"]')
        password = self.browser.find_element_by_xpath('//input[@name="pass"]')
        login = self.browser.find_element_by_xpath('//input[@value="Login"]')

        email.send_keys(EMAIL)
        password.send_keys(PASSWORD)
        login.click()

    def parse_notifications(self):
        self.browser.get('http://jade.astroempires.com/notifications.aspx')
        self.check_page_login_if_needed('Notifications')

        t = tuple(t.text for t in self.browser.find_elements_by_xpath('//td'))
        return zip(t[::2], t[1::2])

    def parse_fleets(self, astro):
        self.browser.get(astro)
        self.check_page_login_if_needed('Map')

        fleets = self.browser.find_element_by_xpath('//div[@id="map_fleets"]')
        t = tuple(t.text for t in fleets.find_elements_by_xpath('.//td'))
        return zip(t[::4], t[1::4], t[2::4], t[3::4])


if __name__ == "__main__":
    spider = Spider()
    for n in spider.parse_fleets('http://jade.astroempires.com/map.aspx?loc=J14:44:99:12'):
        print(n)
