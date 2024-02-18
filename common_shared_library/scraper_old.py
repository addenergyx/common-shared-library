# -*- coding: utf-8 -*-
"""
Created on Wed May 27 09:26:46 2020

@author: david
"""

from selenium import webdriver
from fake_useragent import UserAgent
import os
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from random import randrange
# from selenium.common.exceptions import NoSuchElementException
# from datetime import datetime

load_dotenv(verbose=True, override=True)


def get_driver(headless=False, proxy=False, captcha=False, firefox=False):

    ua = UserAgent(use_cache_server=False)
    user_agent = ua.random

    if firefox:
        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
        from selenium.webdriver import DesiredCapabilities
        profile = FirefoxProfile()
        profile.set_preference('devtools.jsonview.enabled', False)
        PROXY_HOST = "12.12.12.123"
        PROXY_PORT = "1234"
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", PROXY_HOST)
        profile.set_preference("network.proxy.http_port", int(PROXY_PORT))
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
        # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0'
        fire_fox_driver_path = os.path.join(os.path.dirname(os.getcwd()), 'common', 'Drivers', 'geckodriver.exe')
        print(fire_fox_driver_path)
        firefox_option = Options()
        # firefox_option.set_preference("general.useragent.override", user_agent)
        firefox_option.add_argument("--width=1430")
        firefox_option.add_argument("--height=602")
        firefox_option.add_argument("--disable-web-security")
        firefox_option.add_argument("--allow-running-insecure-content")
        firefox_option.add_argument("--window-size=1100,1000")

        if os.name == 'nt':
            # 'nt' is the value for windows
            return webdriver.Firefox(executable_path=fire_fox_driver_path, options=firefox_option)
        else:
            fire_fox_driver_path = os.path.join(os.getcwd(), 'common', 'Drivers', 'geckodriver')
            return webdriver.Firefox(executable_path=fire_fox_driver_path, firefox_profile=profile, options=firefox_option, desired_capabilities=desired)

    from selenium.webdriver.chrome.options import Options
    options = Options()

    options.add_argument('user-agent={}'.format(user_agent))

    ## Headless browser - doesn't pop up
    ## A headless browser is a web browser without a graphical user interface.
    # options.add_argument("--headless")
    if headless:
        options.add_argument('--headless')

    # Full screen
    options.add_argument("--start-maximized")

    # Use to beat reCapcha v3 :)
    if captcha:
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--window-size=1100,1000")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})

    # Proxy to avoid 403 forbidden error
    # if proxy:
    #     prox = proxies[randrange(len(proxies))]
    #     print(prox)
    #     print('--------------------------------')
    #     options.add_argument('--proxy-server={}'.format(prox))

    WORKING_ENV = os.getenv('WORKING_ENV', 'DEV')

    if WORKING_ENV == 'DEV':  # Windows
        return webdriver.Chrome(ChromeDriverManager().install(),
                                options=options)  # automatically use the correct chromedriver by using the webdrive-manager
    else:
        import sys
        sys.path.append(os.path.abspath("/home/pi/.local/lib/python3.7/site-packages/selenium/__init__.py"))
        sys.path.append(os.path.abspath("/usr/local/lib/python3.7/dist-packages/fake_useragent/__init__.py"))

        options.add_argument(
            "--no-sandbox")  # https://stackoverflow.com/questions/22424737/unknown-error-chrome-failed-to-start-exited-abnormally

        # https://ivanderevianko.com/2020/01/selenium-chromedriver-for-raspberrypi
        # https://www.reddit.com/r/selenium/comments/7341wt/success_how_to_run_selenium_chrome_webdriver_on/
        # https://askubuntu.com/questions/1090142/cronjob-unable-to-find-module-pydub
        # https://stackoverflow.com/questions/23908319/run-selenium-with-crontab-python
        return webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
