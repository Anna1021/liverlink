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
from selenium.webdriver.common.keys import Keys
import time

class ConversationJavascriptTest(StaticLiveServerTestCase):
    """Unit tests of javascript in conversation view."""

    fixtures = ['peer_support/tests/fixtures/other_users.json',
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless") 
        # options.add_argument("--disable-cache")
        options.add_argument("--window-size=1920,1080")
        cls.selenium = WebDriver(service=Service(), options=options)
        cls.selenium.maximize_window()
        cls.selenium.implicitly_wait(40)
        cls.wait = WebDriverWait(cls.selenium, 20)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.get(username='@janedoe')
        self.user.first_login = False
        self.second_user = User.objects.get(username='@petrapickles')
        self.conversation = Conversation.objects.create()
        self.conversation.users.add(self.user)
        self.conversation.users.add(self.second_user)
        self.user.conversations.add(self.conversation)
        for i in range(21):
            msg = Message.objects.create(
                sender=self.user,
                content="meow",
            )
            msg.visible_to.add(self.user)
            self.conversation.messages.add(msg)
        self.conversation.save()
        self.user.save()

    def test_hide_messages_from_blocked_users(self):
        self.user.blocked_users.add(self.second_user)
        self.user.save()
        message = Message.objects.create(sender=self.second_user, content='ABC')
        message.visible_to.add(self.user)
        self.conversation.messages.add(message)
    
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
    
    def test_scrolls_to_bottom_at_first_load(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_input.send_keys('@janedoe')
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Messages')]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "@petrapickles"))).click()

            conversation = self.wait.until(EC.presence_of_element_located((By.ID, "conversation")))
            height = int(conversation.get_attribute("scrollHeight"))
            offset = conversation.size['height']
            scroll_bottom = height-offset
            location = self.selenium.execute_script("return arguments[0].scrollTop;",conversation)
            self.assertEqual(location,scroll_bottom)

        
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")
 

    def test_scrolls_to_bottom_when_reload_near_bottom(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_input.send_keys('@janedoe')
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Messages')]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "@petrapickles"))).click()
            
            conversation = self.wait.until(EC.presence_of_element_located((By.ID, "conversation")))
            self.selenium.execute_script("arguments[0].scrollTop -= 100;",conversation)
            location = self.selenium.execute_script("return arguments[0].scrollTop;",conversation)
            height = int(conversation.get_attribute("scrollHeight"))

            offset = conversation.size['height']
            scroll_bottom = height-offset
            self.assertEqual(location,scroll_bottom-100)
            self.selenium.execute_script("window.location.reload();")
            conversation = self.wait.until(EC.presence_of_element_located((By.ID, "conversation")))
            location = self.selenium.execute_script("return arguments[0].scrollTop;",conversation)
            self.assertEqual(location,scroll_bottom)

        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")
         
    def test_same_scroll_when_reload_high_up(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_input.send_keys('@janedoe')
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Messages')]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "@petrapickles"))).click()
            
            conversation = self.wait.until(EC.presence_of_element_located((By.ID, "conversation")))
            self.selenium.execute_script("arguments[0].scrollTop -= 400;",conversation)
            location = self.selenium.execute_script("return arguments[0].scrollTop;",conversation)
            height = int(conversation.get_attribute("scrollHeight"))
            offset = conversation.size['height']
            scroll_bottom = height-offset
            self.assertEqual(location,scroll_bottom-400)
            self.selenium.execute_script("window.location.reload();")
            conversation = self.wait.until(EC.presence_of_element_located((By.ID, "conversation")))
            location = self.selenium.execute_script("return arguments[0].scrollTop;",conversation)
            self.assertEqual(location,scroll_bottom-400)

        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")
    
    def test_scrolls_to_bottom_after_posting_message(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_input.send_keys('@janedoe')
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Messages')]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "@petrapickles"))).click()
            
            conversation = self.wait.until(EC.presence_of_element_located((By.ID, "conversation")))
            self.selenium.execute_script("arguments[0].scrollTop -= 400;",conversation)
            location = self.selenium.execute_script("return arguments[0].scrollTop;",conversation)
            height = int(conversation.get_attribute("scrollHeight"))
            offset = conversation.size['height']
            scroll_bottom = height-offset
            self.assertEqual(location,scroll_bottom-400)

            message_input = self.wait.until(EC.presence_of_element_located((By.ID, "id_content")))
            message_input.send_keys('meow')
            message_input.send_keys(Keys.ENTER)

            conversation = self.wait.until(EC.presence_of_element_located((By.ID, "conversation")))
            location = self.selenium.execute_script("return arguments[0].scrollTop;",conversation)
            height = int(conversation.get_attribute("scrollHeight"))
            scroll_bottom = height-offset
            self.assertEqual(location,scroll_bottom)

        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")
    
    def test_same_scroll_when_load_more_messages(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_input.send_keys('@janedoe')
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Messages')]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "@petrapickles"))).click()
            
            conversation = self.wait.until(EC.presence_of_element_located((By.ID, "conversation")))
            self.selenium.execute_script("arguments[0].scrollTop = 0;",conversation)
            location = self.selenium.execute_script("return arguments[0].scrollTop;",conversation)
            original_height = int(conversation.get_attribute("scrollHeight"))
            self.assertEqual(location,0)

            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "@petrapickles"))).click()

            conversation = self.wait.until(EC.presence_of_element_located((By.ID, "conversation")))
            location = self.selenium.execute_script("return arguments[0].scrollTop;",conversation)
            new_height = int(conversation.get_attribute("scrollHeight"))
            offset = conversation.size['height']
            self.assertEqual(location,new_height-original_height)

        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")

    def test_scrolls_to_bottom_when_scroll_button_pressed(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_input.send_keys('@janedoe')
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Messages')]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "@petrapickles"))).click()
            
            conversation = self.wait.until(EC.presence_of_element_located((By.ID, "conversation")))
            self.selenium.execute_script("arguments[0].scrollTop = 0;",conversation)
            location = self.selenium.execute_script("return arguments[0].scrollTop;",conversation)
            height = int(conversation.get_attribute("scrollHeight"))
            offset = conversation.size['height']
            scroll_bottom = height-offset
            self.assertEqual(location,0)
            scroll_button = self.wait.until(EC.element_to_be_clickable((By.ID,"scroll-down"))).click()
            time.sleep(1)
            location = self.selenium.execute_script("return arguments[0].scrollTop;",conversation)
            self.assertEqual(location,scroll_bottom)

        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")