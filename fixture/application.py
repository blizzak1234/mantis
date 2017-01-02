from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from fixture.session import SessionHelper


class Application:
    def __init__(self, browser, base_url):
        #self.wd = WebDriver(firefox_binary=FirefoxBinary("C:\\Program Files\\FF_ESR\\firefox.exe"))
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.wd.implicitly_wait(1)
        self.session = SessionHelper(self)
        self.base_url = base_url



    def destroy(self):
        self.wd.quit()


    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def change_field_value(self, field_name, text):
        wd = self.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)


    def open_home_page(self):
        wd = self.wd
        # if not (wd.current_url.endswith("/addressbook/") and wd.find_element_by_xpath("//div/div[4]/form[2]/em/strong").text == "Select all"):
        # open home page
        wd.get(self.base_url)