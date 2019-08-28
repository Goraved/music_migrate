import os
import platform

import gevent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager


class Driver:
    @staticmethod
    def get_driver():
        BROWSER = os.getenv('BROWSER', 'chrome')
        driver = None
        operation_system = platform.system()
        arch = platform.architecture()
        if BROWSER == 'chrome':
            options = Options()
            if os.getenv('HEADLESS', 'false').lower() == 'true':
                options.headless = True
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--incognito")
            options.add_argument("--window-size=1920,1080")
            options.add_experimental_option('w3c', False)
            try:
                driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            except:
                gevent.sleep(2)
                driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        elif BROWSER == 'firefox':
            if operation_system == "Darwin" or "Linux":
                driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
            else:
                if arch[0] == "32bit":
                    driver = webdriver.Firefox(executable_path=GeckoDriverManager(os_type="win32").install())
                elif arch[0] == "64bit":
                    driver = webdriver.Firefox(executable_path=GeckoDriverManager(os_type="win64").install())
        elif BROWSER == 'safari':
            driver = webdriver.Safari(executable_path='/usr/bin/safaridriver')
        elif BROWSER == 'ie':
            if arch[0] == "32bit":
                driver = webdriver.Ie(executable_path=IEDriverManager(os_type="Win32").install())
            elif arch[0] == "64bit":
                driver = webdriver.Ie(executable_path=IEDriverManager(os_type="x64").install())
        return Driver.add_driver_settings(driver)

    @staticmethod
    def add_driver_settings(driver):
        gevent.sleep(2)
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(60)
        driver.maximize_window()
        return driver
