from alumnium import Alumni
from selenium.webdriver import Chrome
from robot.api.deco import keyword, library
import os

@library
class AlumniRobotLibrary:
    def __init__(self, openai_api_key=None):
        self.driver = None
        self.al = None
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key

    @keyword
    def open_browser_and_init_alumni(self, url):
        self.driver = Chrome()
        self.driver.get(url)
        self.al = Alumni(self.driver)

    @keyword
    def alumni_do(self, command):
        self.al.do(command)

    @keyword
    def alumni_check(self, check_command):
        self.al.check(check_command)

    @keyword
    def alumni_get(self, get_command):
        return self.al.get(get_command)

    @keyword
    def alumni_quit(self):
        if self.driver:
            self.driver.quit()
