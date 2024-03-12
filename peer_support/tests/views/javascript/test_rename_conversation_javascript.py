"""Unit test of javascript in create_conversation view"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from peer_support.models import User,GroupConversation
from selenium.common.exceptions import TimeoutException

class RenameConversationJavascriptTest(StaticLiveServerTestCase):
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
        cls.selenium = WebDriver(service=Service(), options=options)
        cls.selenium.implicitly_wait(40)
        cls.wait = WebDriverWait(cls.selenium, 20)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_dynamic_form_display(self):
        user = User.objects.get(username='@johndoe')
        user.conversations.set([1,2])
        user.first_login=False
        group_conversation = GroupConversation.objects.get(pk=2)
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            username_input =self.wait.until(EC.element_to_be_clickable((By.NAME, "username")))
            username_input.send_keys('@johndoe')

            password_input =self.wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_input.send_keys('Password123')

            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()

            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Messages')]"))).click()
            conversation_link =self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/conversation/2']")))
            conversation_link.click()

            dropdown_link =self.wait.until(EC.element_to_be_clickable((By.ID, "conversation-dropdown")))
            dropdown_link.click()

            details_link =self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/conversation_details/2']")))
            details_link.click()

            header =self.wait.until(EC.presence_of_element_located((By.XPATH, '//h3[@id="conversation-name"]')))
            form =self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="conversation-name-input"]')))
            
            self.assertEqual(header.value_of_css_property('display'),'block')
            self.assertEqual(form.value_of_css_property('display'),'none')

            toggle =self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="rename-button"]')))
            self.assertEqual(toggle.get_attribute('innerHTML'),'Rename')
            toggle.click()
            self.assertEqual(toggle.get_attribute('innerHTML'),'Cancel')

            self.assertEqual(header.value_of_css_property('display'),'none')
            self.assertEqual(form.value_of_css_property('display'),'block')
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")