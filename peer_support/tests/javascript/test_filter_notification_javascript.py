"""Unit test of javascript in inbox view"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from peer_support.models import User
from selenium.webdriver.chrome.service import Service

class FilterNotificationTest(StaticLiveServerTestCase):
    """Unit test of javascript of dropdown list in inbox view"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
    ]
    
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
    
    def test_filtration_dropdown_update(self):
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
            
            self.wait.until(EC.element_to_be_clickable((By.ID, 'inbox'))).click()

            timeframe_dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, 'notification_timeframe')))
            timeframe_dropdown.click()
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//option[text()='Past 7 Days']"))).click()
            
            type_dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, 'notification_type')))
            type_dropdown.click()
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//option[text()='Friend Request']"))).click()
            
            expected_url = f"{self.live_server_url}/inbox/?timeframe=past_7_days&type=friend%20request"
            self.assertEqual(self.selenium.current_url, expected_url, "URL did not match expected pattern after dropdown selection")
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout: {e}")
        

        
