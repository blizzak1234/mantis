

class NavigationHelper:
    def __init__(self, app):
        self.app = app

    def open_home_page(self):
        wd = self.app.wd
        #if not (wd.current_url.endswith("/addressbook/") and wd.find_element_by_xpath("//div/div[4]/form[2]/em/strong").text == "Select all"):
        # open home page
        wd.get(self.app.base_url)

    def return_to_home(self):
        # return to home page
        wd = self.app.wd
        #if not (wd.current_url.endswith("/addressbook/") and wd.find_element_by_xpath("//div/div[4]/form[2]/em/strong").text == "Select all"):
        # open home page
        wd.get(self.app.base_url)
