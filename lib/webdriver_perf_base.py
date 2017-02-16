"""
The performance unittest cases which based on Web Driver
"""

import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.logConfig import get_logger


logger = get_logger(__name__)


class WebDriverPerfBaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(WebDriverPerfBaseTest, self).__init__(*args, **kwargs)
        self.driver = None

    def setUp(self):
        # WebDriverException: Message: 'geckodriver' executable needs to be in PATH.
        # HOW TO FIX
        # 1. download list https://github.com/mozilla/geckodriver/releases
        #   Linux
        #   - $ wget --output-document=./thirdParty/geckodriver-v0.14.0.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.14.0/geckodriver-v0.14.0-linux64.tar.gz
        #   Mac
        #   - $ wget --output-document=./thirdParty/geckodriver-v0.14.0.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.14.0/geckodriver-v0.14.0-macos.tar.gz
        # 2. Unzip
        #   $ mkdir -p ./thirdParty/geckodriver/
        #   $ tar -xvzf ./thirdParty/geckodriver-v0.14.0.tar.gz -C ./thirdParty/geckodriver/
        # 3. Add exec permission
        #   $ chmod a+x ./thirdParty/geckodriver/geckodriver
        # 4. Add to PATH
        #   $ echo 'PATH="$PATH:'`pwd`'/thirdParty/geckodriver/geckodriver"' >> ~/.bash_profile
        #   $ source ~/.bash_profile
        #
        # TEST RUN
        #   $ python -m unittest discover -s webdriver-tests -v
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.close()
        self.driver.quit()

    @staticmethod
    def wait_for(condition_function):
        start_time = time.time()
        while time.time() < start_time + 10:
            if condition_function():
                return True
            else:
                time.sleep(0.1)
        raise Exception(
            'Timeout waiting for {}'.format(condition_function.__name__)
        )

    def page_has_loaded(self):
        page_state = self.driver.execute_script('return document.readyState;')
        return page_state == 'complete'
