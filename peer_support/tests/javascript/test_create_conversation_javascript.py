"""Unit test of javascript in create_conversation view"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from peer_support.models import User
from selenium.common.exceptions import TimeoutException

class CreateConversationJavascriptTest(StaticLiveServerTestCase):
    """Unit test of javascript in find_friends view"""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/default_conversation.json',
                'peer_support/tests/fixtures/default_group_conversation.json',
                'peer_support/tests/fixtures/default_message.json',
                'peer_support/tests/fixtures/other_messages.json',
    ]

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

    def test_dynamic_button_disabling(self):
        user = User.objects.get(username='@johndoe')
        user.friends.set(User.objects.exclude(username='@johndoe'))
        user.first_login = False
        user.save()
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_input.send_keys('@johndoe')
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Messages')]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/create_conversation/']"))).click()

            direct_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[@id="direct"]')))
            group_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[@id="group"]')))

            self.assertFalse(direct_button.is_enabled())
            self.assertFalse(group_button.is_enabled())

            select_menu = self.wait.until(EC.presence_of_element_located((By.XPATH, '//select[@id="id_users"]')))
            select = Select(select_menu)
            select.select_by_index(0)

            self.wait.until(lambda driver: direct_button.is_enabled())
            self.wait.until(lambda driver: group_button.is_enabled())

            self.assertTrue(direct_button.is_enabled())
            self.assertTrue(group_button.is_enabled())

            select.select_by_index(1)

            self.wait.until_not(lambda driver: direct_button.is_enabled())

            self.assertFalse(direct_button.is_enabled())
            self.assertTrue(group_button.is_enabled())
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")