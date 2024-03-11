from selenium.common.exceptions import NoSuchElementException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LiveTranslationTest(StaticLiveServerTestCase):
    """Unit test of javascript which translates all views which contain navbar"""
    fixtures = ['peer_support/tests/fixtures/default_user.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080") 
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(40)
        cls.wait = WebDriverWait(cls.selenium, 20)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_webpage_translates(self):
        try:
            self.selenium.get(f'{self.live_server_url}/log_in/')
            username_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "username")))
            username_input.send_keys('@johndoe')
            password_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')
            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]')))
            login_button.click()
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for an element: {e}")

        try:
            translate_widget =self.wait.until(EC.presence_of_element_located((By.ID, "google_translate_element")))
        except NoSuchElementException:
            self.fail("Google Translate widget not found on the page.")

    def test_page_reloads_widget_when_navigation_arrows_used(self):
        try:
            self.selenium.get(f'{self.live_server_url}/log_in/')
            username_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "username")))
            username_input.send_keys('@johndoe')
            password_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')
            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]')))
            login_button.click()
            find_friends_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Find Friends')]")))
            find_friends_button.click()
            find_friends_button_again = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Find Friends')]")))
            find_friends_button_again.click()
            self.selenium.back()
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for an element: {e}")

        try:
            translate_widget =self.wait.until(EC.presence_of_element_located((By.ID, "google_translate_element")))
        except NoSuchElementException:
            self.fail("Google Translate widget not found on the page.")

