"""Unit tests of javascript in display_blocklist template of other_user_settings view."""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DisplayBlocklistJavascriptTest(StaticLiveServerTestCase):
    """Unit tests of javascript in display_blocklist template of other_user_settings view."""

    fixtures = ['peer_support/tests/fixtures/other_users.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
       # options.add_argument("--headless") 
        cls.selenium = WebDriver(service=Service(), options=options)
        cls.selenium.maximize_window()
        cls.selenium.implicitly_wait(40)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_dynamic_block_button_change(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('@janedoe')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('Password123')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        self.selenium.find_element(By.XPATH, "//a[@id='user-account-dropdown']/span").click()

        self.selenium.find_element(By.LINK_TEXT, "Settings").click()

        self.selenium.find_element(By.LINK_TEXT, "Other users").click()

        self.selenium.find_element(By.XPATH, "//button[@id='display-blocklist']").click()

        block_toggle_button = self.selenium.find_element(By.CLASS_NAME, "block-user-toggle-btn")

        # test unblock_user GET request: selenium-wire
        self.assertEqual("Unblock", block_toggle_button.get_attribute("innerHTML"))
        self.assertEqual("unblock", block_toggle_button.get_attribute("data-action"))

        block_toggle_button.click()

        self.assertEqual("Block", block_toggle_button.get_attribute("innerHTML"))
        self.assertEqual("block", block_toggle_button.get_attribute("data-action"))

        block_toggle_button.click()

        block_toggle_button = self.selenium.find_element(By.CLASS_NAME, "block-user-toggle-btn") #refresh button

        self.assertEqual("Unblock", block_toggle_button.get_attribute("innerHTML"))
        self.assertEqual("unblock", block_toggle_button.get_attribute("data-action"))