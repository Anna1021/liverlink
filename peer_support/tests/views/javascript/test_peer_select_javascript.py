# """Unit test of javascript in peer_select view"""
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium.webdriver.chrome.webdriver import WebDriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class PeerSelectJavascriptTest(StaticLiveServerTestCase):
#     """Unit test of javascript in peer_select view"""
#     fixtures = ['peer_support/tests/fixtures/default_user.json']

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         options = Options()
#         options.add_argument("--headless") 
#         cls.selenium = WebDriver(service=Service(), options=options)
#         cls.selenium.implicitly_wait(10)
        
#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()

#     def test_dynamic_form_peer_select(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
#         username_input = self.selenium.find_element(By.NAME, "username")
#         username_input.send_keys('@johndoe')
#         password_input = self.selenium.find_element(By.NAME, "password")
#         password_input.send_keys('Password123')
#         self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

#         self.selenium.find_element(By.XPATH, "//button[contains(text(), 'Find Friends')]").click()

#         dropdown_button = self.selenium.find_element(By.XPATH, "//button[@id='dropdownMenuButton']")
#         dropdown_button.click()

#         patient_checkbox = self.selenium.find_element(By.XPATH, '//input[@type="checkbox" and @value="PT"]')
#         if not patient_checkbox.is_selected():
#             patient_checkbox.click()

#         age_of_diagnosis_min_field = WebDriverWait(self.selenium, 10).until(
#             EC.visibility_of_element_located((By.XPATH, "//input[@name='age_of_diagnosis_min']"))
#         )
#         self.assertTrue(age_of_diagnosis_min_field.is_displayed(), "age_of_diagnosis_min field is not visible")

#         parent_checkbox = self.selenium.find_element(By.XPATH, '//input[@type="checkbox" and @value="PR"]')
#         if not parent_checkbox.is_selected():
#             parent_checkbox.click()

#         child_age_of_diagnosis_min_field = WebDriverWait(self.selenium, 10).until(
#             EC.visibility_of_element_located((By.XPATH, "//input[@name='child_age_of_diagnosis_min']"))
#         )
#         self.assertTrue(child_age_of_diagnosis_min_field.is_displayed(), "age_of_diagnosis_min field is not visible")
