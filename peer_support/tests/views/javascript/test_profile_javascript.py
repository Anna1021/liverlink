"""Unit tests of javascript in profile view."""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from peer_support.models import User, FriendRequest, Notification

class ProfileJavascriptTest(StaticLiveServerTestCase):
    """Unit tests of javascript in profile view."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_patient.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/other_parents.json',
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
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_add_friend_sends_request(self):

        user = User.objects.get(username='@janedoe')
        second_user = User.objects.get(username='@petrapickles')
        user.first_login = False
        user.save()

        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('@janedoe')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('Password123')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        self.selenium.find_element(By.XPATH, "//button[contains(text(), 'Find Friends')]").click()

        self.selenium.find_element(By.XPATH, "//a[@href='/profile/@petrapickles/']").click()
       
        self.selenium.find_element(By.ID, "user-actions-dropdown").click()

        friend_link = self.selenium.find_element(By.ID, "friend-link")
        self.assertEqual("Add friend", friend_link.get_attribute("innerHTML"))
        friend_link.click()

        user_actions_dropdown = WebDriverWait(self.selenium, 10).until(
            EC.visibility_of_element_located((By.ID, "user-actions-dropdown"))
        )
        user_actions_dropdown.click()

        friend_link = self.selenium.find_element(By.ID, "friend-link")
        self.assertEqual("Request sent", friend_link.get_attribute("innerHTML"))
        self.assertTrue(FriendRequest.objects.filter(sender=user, receiver=second_user).exists())
        friend_request = FriendRequest.objects.get(sender=user, receiver=second_user)
        self.assertTrue(Notification.objects.filter(friend_request=friend_request).exists())

        Notification.objects.get(friend_request=friend_request).delete()
        friend_request.delete()

    def test_remove_friend(self):

        user = User.objects.get(username='@janedoe')
        second_user = User.objects.get(username='@petrapickles')
        user.friends.add(second_user)
        user.first_login = False
        user.save()

        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('@janedoe')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('Password123')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        self.selenium.find_element(By.XPATH, "//button[contains(text(), 'Friends list')]").click()

        self.selenium.find_element(By.XPATH, "//a[@href='/profile/@petrapickles/']").click()

        self.selenium.find_element(By.ID, "user-actions-dropdown").click()

        friend_link = self.selenium.find_element(By.ID, "friend-link")
        self.assertEqual("Remove friend", friend_link.get_attribute("innerHTML"))
        friend_link.click()

        user_actions_dropdown = WebDriverWait(self.selenium, 10).until(
            EC.visibility_of_element_located((By.ID, "user-actions-dropdown"))
        )
        user_actions_dropdown.click()

        friend_link = self.selenium.find_element(By.ID, "friend-link")
        self.assertEqual("Add friend", friend_link.get_attribute("innerHTML"))
        self.assertNotIn(second_user, user.friends.all())
        self.assertNotIn(user, second_user.friends.all())

    def test_block_user_reloads_page(self):

        user = User.objects.get(username='@janedoe')
        second_user = User.objects.get(username='@petrapickles')
        user.first_login = False
        user.save()

        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('@janedoe')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('Password123')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        self.selenium.find_element(By.XPATH, "//button[contains(text(), 'Find Friends')]").click()

        self.selenium.find_element(By.XPATH, "//a[@href='/profile/@petrapickles/']").click()

        self.selenium.find_element(By.ID, "user-actions-dropdown").click()

        profile_content = self.selenium.find_element(By.ID, "profile-content")
        self.assertIsNotNone(profile_content)

        block_link = self.selenium.find_element(By.ID, "block-link")
        self.assertEqual("Block this user", block_link.get_attribute("innerHTML"))
        block_link.click()

        user_is_blocked = self.selenium.find_element(By.ID, "user-is-blocked")
        self.assertIsNotNone(user_is_blocked)

        user_actions_dropdown = WebDriverWait(self.selenium, 10).until(
            EC.visibility_of_element_located((By.ID, "user-actions-dropdown"))
        )
        user_actions_dropdown.click()

        block_link = self.selenium.find_element(By.ID, "block-link")
        self.assertEqual("Unblock this user", block_link.get_attribute("innerHTML"))
        self.assertIn(second_user, user.blocked_users.all())

        user.blocked_users.remove(second_user)

    def test_unblock_user_reloads_page(self):

        user = User.objects.get(username='@janedoe')
        second_user = User.objects.get(username='@petrapickles')
        user.blocked_users.add(second_user)
        user.first_login = False
        user.save()

        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('@janedoe')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('Password123')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        self.selenium.find_element(By.XPATH, "//a[@id='user-account-dropdown']/span").click()

        self.selenium.find_element(By.LINK_TEXT, "Settings").click()

        self.selenium.find_element(By.LINK_TEXT, "Other users").click()

        self.selenium.find_element(By.XPATH, "//button[@id='display-blocklist']").click()

        self.selenium.find_element(By.XPATH, "//a[@href='/profile/@petrapickles/']").click()

        self.selenium.find_element(By.ID, "user-actions-dropdown").click()

        user_is_blocked = self.selenium.find_element(By.ID, "user-is-blocked")
        self.assertIsNotNone(user_is_blocked)

        block_link = self.selenium.find_element(By.ID, "block-link")
        self.assertEqual("Unblock this user", block_link.get_attribute("innerHTML"))
        block_link.click()

        user_actions_dropdown = WebDriverWait(self.selenium, 10).until(
            EC.visibility_of_element_located((By.ID, "user-actions-dropdown"))
        )
        user_actions_dropdown.click()

        profile_content = self.selenium.find_element(By.ID, "profile-content")
        self.assertIsNotNone(profile_content)

        block_link = self.selenium.find_element(By.ID, "block-link")
        self.assertEqual("Block this user", block_link.get_attribute("innerHTML"))
        self.assertNotIn(second_user, user.blocked_users.all())