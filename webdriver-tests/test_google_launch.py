import time
from lib.webdriver_perf_base import WebDriverPerfBaseTest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class BrowserTester(WebDriverPerfBaseTest):

    def setUp(self):
        super(BrowserTester, self).setUp()
        self.target_url = 'https://www.google.com/'

    def test_google_launch(self):
        self.driver.get(self.target_url)
        assert "Google" in self.driver.title
        print('Current URL: {}'.format(self.driver.current_url))

        print('wait for q')
        self.wait.until(EC.visibility_of_element_located((By.NAME, 'q')))
        query_elem = self.driver.find_element_by_name('q')
        query_elem.send_keys('Askeing github')
        time.sleep(1)

        print('wait for input text')
        self.wait.until(EC.text_to_be_present_in_element_value((By.NAME, 'q'), 'Askeing github'))
        submit_elem = self.driver.find_element_by_name('btnK')
        submit_elem.click()
        time.sleep(1)

        #print('wait for button invisibility')
        #self.wait.until(EC.invisibility_of_element_located((By.NAME, 'btnK')))
        print('wait for search result')
        #self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#search div.g div.rc .r')))
        self.wait_for(self.page_has_loaded)
        search_result_list = self.driver.find_elements_by_css_selector('div#search div.g div.rc .r')
        time.sleep(1)
        match_list = [item for item in search_result_list if 'Askeing Yen' in item.text]
        assert len(match_list) > 0
