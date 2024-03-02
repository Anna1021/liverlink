"""Unit tests of javascript in conversation view."""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
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
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_hide_messages_from_blocked_users(self):

        user = User.objects.get(username='@janedoe')
        second_user = User.objects.get(username='@petrapickles')
        user.blocked_users.add(second_user)

        #Create a conversation containing two users
        conversation = Conversation.objects.create()
        conversation.users.add(user)
        conversation.users.add(second_user)
        message = Message.objects.create(sender=second_user, content='ABC')
        message.visible_to.add(user)
        conversation.messages.add(message)
        user.conversations.add(conversation)
    

        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('@janedoe')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('Password123')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        self.selenium.find_element(By.XPATH, "//button[contains(text(), 'Messages')]").click()

        self.selenium.find_element(By.LINK_TEXT, "@petrapickles").click()

        hidden_message = self.selenium.find_element(By.NAME, "blocked-message")
        self.assertEqual("You have blocked this user. Click to reveal text.", hidden_message.get_attribute("innerHTML"))
        self.assertEqual("text-muted", hidden_message.get_attribute("class"))

        hidden_message.click()
        self.assertEqual(hidden_message.get_attribute("data-text"), hidden_message.get_attribute("innerHTML"))
        self.assertEqual("", hidden_message.get_attribute("class"))
