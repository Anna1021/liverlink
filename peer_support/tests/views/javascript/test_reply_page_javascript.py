"""Unit test of javascript in peer_select view"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time



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
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(10)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_reply_form_toggle(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('@johndoe')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('Password123')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()
        self.selenium.find_element(By.XPATH, "//button[contains(text(), 'Resources')]").click()
        link = self.selenium.find_element(By.XPATH, "//p[@class='question-list-item-title' and contains(text(), 'Sample Question Title')]")
        # link.click()

        wait = WebDriverWait(self.selenium, 10)

        try:
            close_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn-close btn-outline-light" and @data-bs-dismiss="modal"]')))
            close_button.click()
        except ElementClickInterceptedException:
            print("ElementClickInterceptedException caught, waiting and retrying...")
            time.sleep(2) 

        close_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn-close btn-outline-light" and @data-bs-dismiss="modal"]')))
        close_button.click()

        # Find and click the reply button
        # reply_button = WebDriverWait(self.selenium, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'reply')]"))
        # )
        # reply_button.click()

        reply_button = WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".reply-button"))
        )
        reply_button.click()
        reply_form_container = self.selenium.find_element(By.CSS_SELECTOR, ".reply-form-container.enabled")
        self.assertTrue(reply_form_container.is_displayed())
       #self.selenium.find_element(By.XPATH, "//button[contains(text(), 'cancel')]").click()
        cancel_button = self.selenium.find_element(By.CSS_SELECTOR, ".reply-form-cancel-button")
        cancel_button.click()
        reply_form_container = self.selenium.find_element(By.CSS_SELECTOR, ".reply-form-container")
        self.assertFalse(reply_form_container.is_displayed())
