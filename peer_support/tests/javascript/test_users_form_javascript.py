"""Unit test of javascript to add users to a conversation."""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from peer_support.models import User
from selenium.webdriver.chrome.service import Service

class UserFormJavascriptTest(StaticLiveServerTestCase):
    """Unit test of javascript to add users to a conversation."""

    fixtures = [
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_mentor.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/other_parents.json',
        'peer_support/tests/fixtures/other_posts.json',
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

    def test_user_selection(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        user = User.objects.get(username='@petrapickles')
        user.first_login = False
        user.save()
        try:
            username_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "username")))
            username_input.send_keys('@petrapickles')
            password_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()

            self.selenium.get('%s%s' % (self.live_server_url, '/create_conversation/'))   
            select_menu = self.wait.until(EC.presence_of_element_located((By.XPATH, '//select[@id="id_users"]')))
            select = Select(select_menu)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//option[@value='4']"))).click()
            selected_options = select.all_selected_options
            self.assertEqual(len(selected_options),1)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//option[@value='5']"))).click()
            selected_options = select.all_selected_options
            self.assertEqual(len(selected_options),2)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//option[@value='5']"))).click()
            selected_options = select.all_selected_options
            self.assertEqual(len(selected_options),1)

        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")