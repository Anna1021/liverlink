"""Unit test of javascript in inbox view"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from peer_support.models import User

class FilterNotificationTest(StaticLiveServerTestCase):
    """Unit test of javascript of dropdown list in inbox view"""

    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/default_notification.json',
                'peer_support/tests/fixtures/other_notifications.json'
                ]
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        #options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(50)
        cls.wait = WebDriverWait(cls.selenium, 20)
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    def test_filtration_dropdown_update(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        user = User.objects.get(username='@johndoe')
        user.friends.set(User.objects.exclude(username='@johndoe'))
        user.first_login = False
        user.save()
        
        try:
            # Wait for the dropdowns to load
            timeframe_dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, 'notification_timeframe')))
            type_dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, 'notification_type')))
            
            # Simulate selecting options in the dropdowns
            timeframe_dropdown.click()
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//option[text()='Past 7 Days']"))).click()
            type_dropdown.click()
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//option[text()='Friend Request']"))).click()
            
            # Verify that the URL changes after selecting options
            expected_url = self.live_server_url + '/inbox/?timeframe=past_7_days&type=friend+request'
            self.assertEqual(self.selenium.current_url, expected_url)
        except TimeoutException as e:
                self.fail(f"Test failed due to timeout: {e}")


        
