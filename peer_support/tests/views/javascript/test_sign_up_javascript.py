"""Unit test of javascript in sign up view"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

class SignUpJavascriptTest(StaticLiveServerTestCase):
    """Unit test of javascript in sign up view"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless") 
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(10)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_dynamic_form_sign_up(self):
        wait = WebDriverWait(self.selenium, 10)
        self.selenium.get('%s%s' % (self.live_server_url, '/sign_up/'))

        dropdown_element = wait.until(EC.presence_of_element_located((By.ID, 'id_user_type')))
        actions = ActionChains(self.selenium)
        actions.move_to_element(dropdown_element).perform()
        select = Select(dropdown_element)

        select.select_by_visible_text('Patient')
        age_of_diagnosis=wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='age_of_diagnosis']"))
        )
        self.assertTrue(age_of_diagnosis.is_displayed(), "age_of_diagnosis field is not visible")


        select.select_by_visible_text('Parent')
        child_age_of_diagnosis = wait.until(
            EC.visibility_of_element_located((By.XPATH,"//input[@name='child_age_of_diagnosis']"))
        )
        self.assertTrue(child_age_of_diagnosis.is_displayed(), "child_age_of_diagnosis field is not visible")

        select.select_by_visible_text('Mentor')
        Mentor_age_of_diagnosis=WebDriverWait(self.selenium, 10).until(
            EC.visibility_of_element_located((By.XPATH,"//input[@name='age_of_diagnosis']"))
        )
        self.assertTrue(Mentor_age_of_diagnosis.is_displayed(), "age_of_diagnosis_min field is not visible")
