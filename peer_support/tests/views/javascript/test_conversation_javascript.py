"""Unit tests of javascript in conversation view."""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from peer_support.models import User, Conversation, Message

class ConversationJavascriptTest(StaticLiveServerTestCase):
    """Unit tests of javascript in conversation view."""

    fixtures = ['peer_support/tests/fixtures/other_users.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless") 
        options.add_argument("--window-size=1920,1080")
        cls.selenium = WebDriver(service=Service(), options=options)
        cls.selenium.maximize_window()
        cls.selenium.implicitly_wait(40)
        cls.wait = WebDriverWait(cls.selenium, 20)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_hide_messages_from_blocked_users(self):
        user = User.objects.get(username='@janedoe')
        second_user = User.objects.get(username='@petrapickles')
        user.blocked_users.add(second_user)
        user.first_login = False
        user.save()

        conversation = Conversation.objects.create()
        conversation.users.add(user)
        conversation.users.add(second_user)
        message = Message.objects.create(sender=second_user, content='ABC')
        message.visible_to.add(user)
        conversation.messages.add(message)
        user.conversations.add(conversation)
    
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_input.send_keys('@janedoe')
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Messages')]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "@petrapickles"))).click()

            hidden_message = self.wait.until(EC.presence_of_element_located((By.NAME, "blocked-message")))
            self.assertEqual("You have blocked this user. Click to reveal text.", hidden_message.get_attribute("innerHTML"))
            self.assertEqual("text-muted", hidden_message.get_attribute("class"))
            hidden_message.click()

            self.assertEqual(hidden_message.get_attribute("data-text"), hidden_message.get_attribute("innerHTML"))
            self.assertEqual("", hidden_message.get_attribute("class"))
        
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")