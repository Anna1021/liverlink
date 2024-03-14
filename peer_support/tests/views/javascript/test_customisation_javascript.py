"""Unit test of javascript in customisation view"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(40)
        cls.wait = WebDriverWait(cls.selenium, 40)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_dynamic_button_disabling(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_input.send_keys('@johndoe')
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')
            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]')))
            login_button.click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='user-account-dropdown']/span"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Settings"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Customisation"))).click()
            selected_picture = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[5]/div/img")))
            selected_picture.click()
            
            selected_picture_parent = selected_picture.find_element(By.XPATH, "..") 
            self.assertTrue("picture-selected" in selected_picture_parent.get_attribute("class"), "Selected picture does not have the expected 'picture-selected' class.")
            update_button = self.wait.until(EC.element_to_be_clickable((By.ID, "update-button")))
            self.selenium.execute_script("arguments[0].click();", update_button)
            WebDriverWait(self.selenium, 10).until(EC.alert_is_present(),
                                                    "Timed out waiting for profile picture update confirmation alert.")
            alert = self.selenium.switch_to.alert
            self.assertEqual("Profile picture updated successfully!", alert.text)
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")
