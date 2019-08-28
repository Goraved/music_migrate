import time

import gevent
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidElementStateException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    timeout_sec = 15

    def __init__(self, driver):
        self.driver = driver

    # Open page by full url
    def go_to_exact_url(self, url=""):
        self.driver.get(url)

    # Find element on page
    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    # Find array of elements on page (useful for table, lists, dropdowns etc.)
    def find_elements(self, *locator):
        return self.driver.find_elements(*locator)

    # Click on web element
    def click(self, *locator):
        self.wait_until_element_to_be_clickable(locator)
        self.driver.find_element(*locator).click()

    # Enter text to web element (textbox, text area etc.)
    def type(self, text, *locator):
        self.wait_until_element_is_visible(locator)
        element = self.driver.find_element(*locator)
        try:
            element.clear()
        except InvalidElementStateException:
            pass
        element.send_keys(text)

    # Upload file to upload form
    def upload_file(self, filename, *locator):
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(filename)

    # Clear text field of element
    def clear(self, *locator):
        element = self.driver.find_element(*locator)
        element.clear()

    # Scroll to web element
    def move_to_element(self, *locator):
        element = self.driver.find_element(*locator)
        ActionChains(self.driver).move_to_element(element).perform()

    # Check that checkbox is selected
    def is_selected(self, *locator):
        element = self.driver.find_element(*locator)
        return element.is_selected()

    # Check that element is enabled
    def is_enabled(self, *locator):
        element = self.driver.find_element(*locator)
        return element.is_enabled()

    # Get title of HTML page
    def get_title(self):
        return self.driver.title

    # Get current url of a page
    def get_current_url(self):
        return self.driver.current_url

    # Hove on web element
    def hover(self, *locator):
        self.wait_until_element_is_visible(locator)
        element = self.driver.find_element(*locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    # Check that web element is present on the page
    def is_element_present(self, *locator):
        timeout = self.timeout_sec
        try:
            self.timeout_sec = 1
            self.find_element(*locator)
        except NoSuchElementException:
            self.timeout_sec = timeout
            return False
        self.timeout_sec = timeout
        return True

    # Wait until web element present on page (loader)
    def wait_until_element_present(self, *locator):
        self.driver.implicitly_wait(1)
        try:
            cycle = 0
            while self.is_element_present(*locator):
                time.sleep(0.1)
                cycle += 1
                if cycle > 100:
                    raise NameError('Loader was present too long, more than 10 seconds')
        finally:
            self.driver.implicitly_wait(self.implicit_sec)

    # Wait until element will not be visible on the page
    def wait_until_element_is_visible(self, locator, timeout=timeout_sec):
        try:
            _d = self.driver
            WebDriverWait(_d, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise AssertionError('Element missed. It takes more than {} sec to load an element'.format(timeout))

    # Check if element is invisible on the page
    def is_element_invisible(self, *locator):
        try:
            self.wait_until_invisibility_of_element_located(locator)
            self.find_element(*locator)
        except NoSuchElementException:
            return False
        return True

    # Check if element is visible on the page
    def is_element_visible(self, *locator):
        try:
            self.wait_until_visibility_of_element_located(locator, timeout=1)
        except:
            return False
        return True

    # Wait until element will not be clickable on the page
    def wait_until_element_to_be_clickable(self, *locator, timeout=timeout_sec):
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(*locator))
        except TimeoutException:
            raise AssertionError('Element missed. It takes more than {} sec to load an element'.format(timeout))

    # Wait until element be present not only in DOM, but on page also, and will have width and height > 0
    def wait_until_visibility_of_element_located(self, locator, timeout=timeout_sec):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise AssertionError('Element missed. It takes more than {} sec to load an element'.format(timeout))

    # Wait until element be invisible
    def wait_until_invisibility_of_element_located(self, locator, timeout=timeout_sec):
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            raise AssertionError('Element missed. It takes more than {} sec to load an element'.format(timeout))

    # Get text from web element
    def get_text(self, *locator):
        for _ in range(2):
            try:
                element = self.find_element(*locator)
                return element.text
            except:
                self.press_down()

    # Check if pop up present
    def is_popup_present(self, *locator, timeout=timeout_sec):
        _d = self.driver
        try:
            WebDriverWait(_d, timeout).until(lambda _d: _d.find_element(*locator))
        except Exception:
            return False
        return True

    # Hit "ENTER" button on web element
    def press_enter(self, *locator):
        self.driver.find_element(*locator).send_keys(Keys.ENTER)

    # Hit "DOWN" button on web element
    def press_down(self, click_count=1):
        for _ in range(click_count):
            ActionChains(self.driver).key_down(Keys.ARROW_DOWN).key_up(Keys.ARROW_DOWN).perform()

    # Close system alerts like "Are you sure you want to leave this page?"
    def close_alert(self):
        self.driver.switch_to.alert.accept()

    # Scroll to the top of the page
    def scroll_page_up(self):
        for i in range(0, 3):
            ActionChains(self.driver).key_down(Keys.PAGE_UP).key_up(Keys.PAGE_UP).perform()

    # Scroll to the bottom of the page
    def scroll_page_down(self):
        for i in range(0, 15):
            ActionChains(self.driver).key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()

    def scroll_page_playlist(self, *locator):
        for i in range(0, 40):
            if self.is_element_visible(*locator):
                gevent.sleep(2)
            ActionChains(self.driver).key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()

    # Get count of elements by locator
    def get_number_of_elements(self, *locator):
        self.driver.implicitly_wait(self.implicit_sec)
        number_of_elements = len(self.driver.find_elements(*locator))
        self.driver.implicitly_wait(self.implicit_sec)
        return number_of_elements

    # Remove web element using JS
    def remove_web_item(self, *locator):
        element = self.driver.find_element(*locator)
        self.driver.execute_script("""
var element = arguments[0];
element.parentNode.removeChild(element);
""", element)

    # Focus recently opened tab
    def focus_active_tab(self):
        self.driver.switch_to_window(self.driver.window_handles[-1])

    # Select value from dropdown by value
    def select_by_value(self, value, *locator):
        select = Select(self.driver.find_element(*locator))
        select.select_by_value(value)

    # Get attribute needed value from
    def get_attribute_value(self, attribute, *locator):
        element = self.driver.find_element(*locator)
        return element.get_attribute(attribute)

    @staticmethod
    def get_parametrized_locator(locator, parameter):
        return locator[0], locator[1].format(*parameter)

    @staticmethod
    def compare_songs(expected, actual):
        if str(expected['title']).lower() == str(actual['title']).lower() and str(expected['artist']).lower() == str(
                actual['artist']).lower():
            #  and str(expected['album']).lower() == str(actual['album']).lower()
            return True
        else:
            return False
