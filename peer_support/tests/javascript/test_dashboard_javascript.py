"""Unit test of javascript in dashboard view"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from peer_support.models import User
from selenium.webdriver.chrome.service import Service

class DashboardTutorialJavascriptTest(StaticLiveServerTestCase):
    """Unit test of javascript in dashboard view"""

    fixtures = [
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_mentor.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/other_parents.json',
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

    def test_tutorial_displayed_on_first_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        user = User.objects.get(username='@johndoe')
        user.first_login = True
        user.save()
        try:
            username_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "username")))
            username_input.send_keys('@johndoe')
            password_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            modal =  self.wait.until(
                EC.visibility_of_element_located((By.ID, "tutorialModal")))
            if not modal.is_displayed():
                self.fail("Tutorial didn't display")
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")
        
    def test_tutorial_not_displayed_if_not_first_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        user = User.objects.get(username='@admin')
        user.first_login = False
        user.save()
        try:
            username_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "username")))
            username_input.send_keys('@admin')
            password_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()

            page_source = self.selenium.page_source
            if "tutorialModal" in page_source:
                self.fail("Tutorial modal is unexpectedly present in the page source.")
            
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")