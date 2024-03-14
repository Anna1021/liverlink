"""Unit tests of javascript in display_blocklist template of other_user_settings view."""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from peer_support.models import User
from selenium.common.exceptions import TimeoutException

class DisplayBlocklistJavascriptTest(StaticLiveServerTestCase):
    """Unit tests of javascript in display_blocklist template of other_user_settings view."""

    fixtures = ['peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/other_user_profiles.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless") 
        options.add_argument("--window-size=1920,1080")
        cls.selenium = WebDriver(service=Service(), options=options)
        cls.selenium.maximize_window()
        cls.selenium.implicitly_wait(40)
        cls.wait=WebDriverWait(cls.selenium, 20)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_dynamic_block_button_change(self):

        user = User.objects.get(username='@janedoe')
        blocked_user = User.objects.get(username='@peterpickles')
        user.first_login = False
        user.save()

        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            self.wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys('@janedoe')
            self.wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='user-account-dropdown']/span"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Settings"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Other users"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='display-blocklist']"))).click()

            block_toggle_button = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "block-user-toggle-btn")))

            self.assertIn(blocked_user, user.blocked_users.all())
            self.assertEqual(1, user.blocked_users.all().count())
            self.assertEqual("Unblock", block_toggle_button.get_attribute("innerHTML"))
            self.assertEqual("unblock", block_toggle_button.get_attribute("data-action"))
            self.assertIn("btn-unblock", block_toggle_button.get_attribute("class"))

            block_toggle_button.click()

            block_toggle_button = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "block-user-toggle-btn")))

            self.assertNotIn(blocked_user, user.blocked_users.all())
            self.assertEqual(0, user.blocked_users.all().count())
            self.assertEqual("Block", block_toggle_button.get_attribute("innerHTML"))
            self.assertEqual("block", block_toggle_button.get_attribute("data-action"))
            self.assertIn("btn-block", block_toggle_button.get_attribute("class"))

            block_toggle_button.click()

            block_toggle_button = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "block-user-toggle-btn")))

            self.assertIn(blocked_user, user.blocked_users.all())
            self.assertEqual(1, user.blocked_users.all().count())
            self.assertEqual("Unblock", block_toggle_button.get_attribute("innerHTML"))
            self.assertEqual("unblock", block_toggle_button.get_attribute("data-action"))
            self.assertIn("btn-unblock", block_toggle_button.get_attribute("class"))
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")