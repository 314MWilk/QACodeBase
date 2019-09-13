import ast
import os
import time
from configparser import ConfigParser

from selenium import webdriver


def get_driver_config(path="Configs/drivers.ini"):
    """This will return driver details from Configs/drivers.ini file as a dict"""
    result = {}
    browsers = ConfigParser()
    browsers.read(path)
    result['browser'] = browsers['BROWSER_OPTIONS']['browser']
    result['headless'] = ast.literal_eval(browsers['BROWSER_OPTIONS']['headless'])
    result['full_screen'] = ast.literal_eval(browsers['BROWSER_OPTIONS']['full_screen'])
    result['width'] = ast.literal_eval(browsers['BROWSER_OPTIONS']['width'])
    result['height'] = ast.literal_eval(browsers['BROWSER_OPTIONS']['height'])
    result['download_path'] = browsers['BROWSER_OPTIONS']['download_path']
    result['browser_drivers_path'] = {}
    for key, value in browsers['DRIVERS_PATH'].items():
        result['browser_drivers_path'][key] = value
    return result


def get_driver(driver_config):
    """
    Returns engine for given driver config
    :param driver_config: result of get_driver_config() method
    :return:
    """
    web_driver = select_browser(driver_config)
    time.sleep(1)
    return web_driver


def select_browser(driver_config):
    """
    Method to choose browser and its parameters
    :param driver_config: result of get_driver_config() method
    :return: tuple (chosen_driver, full_screen_setting, width_of_screen, height_of_screen)
    """
    selected_browser = driver_config['browser']
    browser_drivers_path = driver_config['browser_drivers_path']
    height = driver_config['height']
    width = driver_config['width']
    full_screen = driver_config['full_screen']
    headless = driver_config['headless']
    download_path = driver_config['download_path']
    if selected_browser == 'Firefox':
        web_driver = select_firefox(download_path, headless, full_screen, height, width, browser_drivers_path)
    elif selected_browser == 'Chrome':
        web_driver = select_chrome(download_path, headless, full_screen, height, width, browser_drivers_path)
    else:
        raise NotImplementedError('Browser : "{}" is not supported yet, please contact '
                                  'administrator'.format(selected_browser))
    return web_driver


def select_firefox(download_path, headless, full_screen, height, width, browser_drivers_path):
    """
     Method to choose given options for Firefox browser
    :param download_path: path where downloaded files will be saved
    :type headless: bool
    :type full_screen: bool
    :type height: int
    :type width: int
    :param browser_drivers_path: path to browser executable file.
    """
    from selenium.webdriver.firefox.options import Options
    firefox_options = Options()
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", download_path)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream;application/pdf;")
    profile.set_preference("browser.helperApps.alwaysAsk.force", False)
    profile.set_preference("pdfjs.disabled", True)

    if headless:
        os.environ['MOZ_HEADLESS'] = '1'
    if full_screen:
        firefox_options.add_argument("--start-maximized")
    else:
        firefox_options.add_argument("--window-size={},{}".format(height, width))
    return webdriver.Firefox(firefox_profile=profile,
                             options=firefox_options,
                             executable_path=browser_drivers_path['firefox'])


def select_chrome(download_path, headless, full_screen, height, width, browser_drivers_path):
    """
    Method to choose given options for Chrome browser
    :param download_path: path where downloaded files will be saved
    :type headless: bool
    :type full_screen: bool
    :type height: int
    :type width: int
    :param browser_drivers_path: path to browser executable file.
    """
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    preferences = {'download.default_directory': download_path}
    chrome_options.add_experimental_option('prefs', preferences)
    if headless:
        chrome_options.add_argument("--headless")
    if full_screen:
        chrome_options.add_argument("--start-maximized")
    else:
        chrome_options.add_argument("--window-size={},{}".format(height, width))
    return webdriver.Chrome(options=chrome_options,
                            executable_path=browser_drivers_path['chrome'])
