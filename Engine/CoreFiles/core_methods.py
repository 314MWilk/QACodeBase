import calendar
import time

from selenium.common.exceptions import StaleElementReferenceException, InvalidElementStateException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def waiter(func):
    """
    Decorator that waits for page to be fully loaded.
    :param func: any given function that needs waiting for page to be loaded
    :return: Result of given func - in most cases engine for view that application was waiting for being loaded
    """
    def _func(other, *args, **kwargs):
        result = func(other, *args, **kwargs)
        raise_error = 0
        while result.driver.web_driver.execute_script("""return document.readyState;""") != 'complete':
            raise_error += 1
            if raise_error <= 1000:
                raise TimeoutError
            time.sleep(0.01)
        return result
    return _func


def wait_for_element(driver, pointer, xpath=False, timeout=10):
    """Method to wait for elements to be clickable.
    :param driver
    :param pointer: pointer for element
    :param xpath: if True pointer should be given as xpath else it should be selector
    :param timeout: max number of seconds to wait for element
    """
    wait = WebDriverWait(driver, timeout)
    from selenium.webdriver.support import expected_conditions as EC
    for i in range(timeout*10):
        try:
            try:
                if xpath:
                    wait.until(EC.element_to_be_clickable((By.XPATH, pointer)))
                else:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, pointer)))
                break
            except StaleElementReferenceException:
                time.sleep(0.1)
        except InvalidElementStateException:
            time.sleep(0.1)


@waiter
def switch_tab(driver, number):
    """
    Allows driver to change tabs in browser
    :param driver
    :param number: number of tab to be changed for
    """
    time.sleep(2)
    windows = driver.web_driver.window_handles
    driver.web_driver.switch_to.window(windows[number])
    current_window_handler = driver.web_driver.current_window_handle
    driver.web_driver.switch_to_window(current_window_handler)
    return driver


def get_options_from_select(select):
    time.sleep(1)
    return list(map(lambda option: option.text, select.options))


def convert_date_to_timestamp(date, text='%Y-%m-%d %H:%M:%S'):
    """Returns timestamp version of given date that has format yyyy-mm-dd hh:mm:ss"""
    return calendar.timegm(time.strptime(date, text)) - 3600


def convert_timestamp_to_date(timestamp, text='%Y-%m-%d %H:%M:%S'):
    """
    Converts timestamp to date values
    :param timestamp: given timestamp value
    :return: Date in format dd{sign}mm{sign}yyyy{middle_sign}%H:%M:%S or yyyy{sign}mm{sign}{middle_sign}dd%H:%M:%S
    """
    return time.strftime(text, time.localtime(timestamp - 3600))


