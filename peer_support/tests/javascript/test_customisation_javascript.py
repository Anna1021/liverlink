"""Unit test of javascript in customisation view"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from peer_support.models import User
from selenium.webdriver.chrome.service import Service

class CustomisationJavascriptTest(StaticLiveServerTestCase):
    """Unit test of javascript in customisation view"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_patient.json',
        'peer_support/tests/fixtures/default_user_profile.json'
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

    def test_profile_picture_updates(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        user = User.objects.get(username='@johndoe')
        user.first_login = False
        user.save()
        try:
            self.wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys('@johndoe')
            self.wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='user-account-dropdown']/span"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Settings"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Customisation"))).click()
            old_picture = self.wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='Your profile picture']")))
            selected_picture = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='Profile Picture']")))
            selected_picture.click()
            
            selected_picture_parent = selected_picture.find_element(By.XPATH, "..") 
            self.assertTrue("picture-selected" in selected_picture_parent.get_attribute("class"), "Selected picture does not have the expected 'picture-selected' class.")
            update_button = self.wait.until(EC.element_to_be_clickable((By.ID, "update-button")))
            update_button.click()
            WebDriverWait(self.selenium,10).until(EC.staleness_of(update_button))
            new_picture = self.wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='Your profile picture']")))
            self.assertNotEqual(old_picture,new_picture)
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")
