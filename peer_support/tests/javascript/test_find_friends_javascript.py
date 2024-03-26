"""Unit test of javascript in find_friends view"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from peer_support.models import User

class FindFreindsJavascriptTest(StaticLiveServerTestCase):
    """Unit test of javascript in find_friends view"""

    fixtures = ['peer_support/tests/fixtures/default_user.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless") 
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(40)
        cls.wait = WebDriverWait(cls.selenium, 20)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_dynamic_form_find_friends(self):
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
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Find Friends')]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='dropdownMenuButton']"))).click()

            patient_checkbox = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="checkbox" and @value="PT"]')))
            if not patient_checkbox.is_selected():
                patient_checkbox.click()

            age_of_diagnosis_min_field = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='age_of_diagnosis_min']")))
            assert age_of_diagnosis_min_field.is_displayed(), "age_of_diagnosis_min field is not visible"

            parent_checkbox = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="checkbox" and @value="PR"]')))
            if not parent_checkbox.is_selected():
                parent_checkbox.click()

            child_age_of_diagnosis_min_field = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='child_age_of_diagnosis_min']")))
            assert child_age_of_diagnosis_min_field.is_displayed(), "child_age_of_diagnosis_min field is not visible"

            mentor_checkbox = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="checkbox" and @value="MT"]')))
            self.selenium.execute_script("arguments[0].click();", mentor_checkbox)
            
            Mentor_age_of_diagnosis_min_field = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='mentor_age_of_diagnosis_min']")))
            assert Mentor_age_of_diagnosis_min_field.is_displayed(), "mentor_age_of_diagnosis_min field is not visible"

            professional_checkbox = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="checkbox" and @value="PF"]')))
            self.selenium.execute_script("arguments[0].click();", professional_checkbox)
            
            expertise_field = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//select[@name='professional_expertise']")))
            assert expertise_field.is_displayed(), "expertise field is not visible"

            dropdown_element = self.wait.until(EC.presence_of_element_located((By.ID, 'id_location')))
            select = Select(dropdown_element)
            select.select_by_visible_text('United Kingdom')

            hospital_field = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//select[@name='hospital']")))
            self.assertTrue(hospital_field.is_displayed(), "Hospital field is not visible for GB selection")

        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while self.waiting for the question to be visible or interactable: {e}")
