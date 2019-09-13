import inspect
import os
from configparser import ConfigParser
from pathlib import Path

from Engine.CoreFiles.browser_settings import get_driver

cwd = Path(__file__).parents[2]
os.chdir(str(cwd))
credentials = ConfigParser()


class OpenLeoCode:
    """Class to easy start WebShop page using 'with' statement"""

    def __init__(self, driver_config):
        self.driver = get_driver(driver_config)

    def __enter__(self):
        self.driver.get('http://leocode.com')
        from Engine.QAGuild.main_page import MainPage
        return MainPage(self.driver)

    def __exit__(self, type, value, tb):
        """Closes web_driver during leaving with statement, if there is any error it is saved with test case name in
        Results/ScreenResults/ folder as png file"""
        if value:
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            self.driver.get_screenshot_as_file('ScreenResults/{}.png'.format(calframe[1][3]))
        self.driver.quit()
