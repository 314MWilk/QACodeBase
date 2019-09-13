from selenium.webdriver.android.webdriver import WebDriver

from Engine.CoreFiles.core_methods import waiter


class UpperMenu:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    @property
    def blog_button_selector(self):
        return '#menu-item-156 > a'

    @property
    def blog_button(self):
        return self.driver.find_element_by_css_selector(self.blog_button_selector)

    @waiter
    def click_on_blog(self):
        self.blog_button.click()
        from Engine.QAGuild.blog import Blog
        return Blog(self.driver)

    @property
    def get_home_selector(self):
        return '#menu-item-544 > a'

    @property
    def home_button(self):
        return self.driver.find_element_by_css_selector(self.get_home_selector)

    @waiter
    def home(self):
        self.home_button.click()
        from Engine.QAGuild.main_page import MainPage
        return MainPage(self.driver)
