"""Unit test of javascript in peer_select view"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class ReplyPageTest(StaticLiveServerTestCase):
    """Unit test of javascript in reply_page view"""
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/default_question.json',
                'peer_support/tests/fixtures/default_response.json'
                ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless") 
        options.add_argument("--window-size=1920,1080")
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(50)
        cls.wait = WebDriverWait(cls.selenium, 20)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_reply_form_toggle(self):
        try:
            self.selenium.get(f'{self.live_server_url}/log_in/')
            username_input =self.wait.until(EC.visibility_of_element_located((By.NAME, "username")))
            username_input.send_keys('@johndoe')

            password_input =self.wait.until(EC.visibility_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')

            login_button =self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]')))
            login_button.click()

            resources_button =self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Resources')]")))
            resources_button.click()

            link =self.wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='question-list-item-title' and contains(text(), 'Sample Question Title')]")))
            link.click()

            reply_button =self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".reply-button")))
            reply_button.click()

            reply_form_container =self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".reply-form-container.enabled")))
            self.assertTrue(reply_form_container.is_displayed())

            cancel_button =self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".reply-form-cancel-button")))
            cancel_button.click()

            self.wait.until_not(lambda driver: driver.find_element(By.CSS_SELECTOR, ".reply-form-container.enabled").is_displayed())
        
            reply_form_container = self.selenium.find_element(By.CSS_SELECTOR, ".reply-form-container")
            self.assertFalse(reply_form_container.get_attribute("class").endswith("enabled"))
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")



