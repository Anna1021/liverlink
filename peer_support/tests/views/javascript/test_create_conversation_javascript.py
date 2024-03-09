"""Unit test of javascript in create_conversation view"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from peer_support.models import User
from selenium.webdriver.common.keys import Keys

class CreateConversationJavascriptTest(StaticLiveServerTestCase):
    """Unit test of javascript in peer_select view"""
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
        cls.selenium.implicitly_wait(10)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_dynamic_button_disabling(self):
        user = User.objects.get(username='@johndoe')
        user.friends.set(User.objects.exclude(username='@johndoe'))
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('@johndoe')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('Password123')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        self.selenium.find_element(By.XPATH, "//button[contains(text(), 'Messages')]").click()
        #find options
        create_conversation_link = self.selenium.find_element(By.XPATH, "//a[@href='/create_conversation/']")
        create_conversation_link.click()

        direct_button = self.selenium.find_element(By.XPATH, '//button[@id="direct"]')
        group_button = self.selenium.find_element(By.XPATH, '//button[@id="group"]')

        self.assertFalse(direct_button.is_enabled())
        self.assertFalse(group_button.is_enabled())

        select_menu = self.selenium.find_element(By.XPATH, '//select[@id="id_users"]')
        select = Select(select_menu)
        select.select_by_index(0)

        self.assertTrue(direct_button.is_enabled())
        self.assertTrue(group_button.is_enabled())

        Keys.CONTROL
        select.select_by_index(1)

        self.assertFalse(direct_button.is_enabled())
        self.assertTrue(group_button.is_enabled())

