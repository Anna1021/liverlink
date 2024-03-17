"""Unit test of javascript in sign up view"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

class SignUpJavascriptTest(StaticLiveServerTestCase):
    """Unit test of javascript in sign up view"""

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

    def test_dynamic_form_sign_up(self):
        try:
            self.selenium.get(f'{self.live_server_url}/sign_up/')
            dropdown_element = self.wait.until(EC.presence_of_element_located((By.ID, 'id_user_type')))
            select = Select(dropdown_element)

            select.select_by_visible_text('Mentor')
            mentor_age_of_diagnosis = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='referral_code']")))
            self.assertTrue(mentor_age_of_diagnosis.is_displayed(), "Referral code field is not visible for Mentor")

            select.select_by_visible_text('Professional')
            mentor_age_of_diagnosis = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='referral_code']")))
            self.assertTrue(mentor_age_of_diagnosis.is_displayed(), "Referral code field is not visible for Professional")

        except TimeoutException as e:
            self.fail(f"Test failed due to an unexpected exception: {e}")