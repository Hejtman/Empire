from selenium import webdriver

from config import EMAIL, PASSWORD


class Spider:
    def __init__(self):
        self.browser = webdriver.Firefox()

    def __del__(self):
        self.browser.close()

    def login(self):
        email = self.browser.find_element_by_xpath('//input[@name="email"]')
        password = self.browser.find_element_by_xpath('//input[@name="pass"]')
        login = self.browser.find_element_by_xpath('//input[@value="Login"]')

        email.send_keys(EMAIL)
        password.send_keys(PASSWORD)
        login.click()

    def parse_notifications(self):
        self.browser.get('http://jade.astroempires.com/notifications.aspx')
        if self.browser.title == 'Login':
            self.login()
        if self.browser.title != 'Notifications':
            raise ValueError(self.browser.title)

        t = tuple(t.text for t in self.browser.find_elements_by_xpath('//td'))
        return zip(t[::2], t[1::2])


if __name__ == "__main__":
    spider = Spider()
    for n in spider.parse_notifications():
        print(n)
