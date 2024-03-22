"""Unit test of javascript in peer_select view"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from peer_support.models import User
import time

class PeerSelectJavascriptTest(StaticLiveServerTestCase):
    """Unit test of javascript in peer_select view"""

    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/default_post.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        #options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")  
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(40)
        cls.wait = WebDriverWait(cls.selenium, 20)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_dynamic_form_peer_select(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        user = User.objects.get(username='@johndoe')
        user.first_login = False
        user.save()
        try:
            username_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "username")))
            username_input.send_keys('@johndoe')
            password_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'like-post')))

            like_count_element = self.wait.until(EC.presence_of_element_located((By.ID, 'like-count-1'))) 
            initial_like_count = int(like_count_element.text)
            like_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'like-post')))
            like_button.click()
            
            def like_count_increased(driver):
                try:
                    return int(driver.find_element(By.ID, 'like-count-1').text) == initial_like_count + 1
                except ValueError:
                    return False

            self.wait.until(like_count_increased)
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout: {e}")