"""Unit tests of javascript in profile view."""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from peer_support.models import User, FriendRequest, Notification
from django.contrib.contenttypes.models import ContentType
from selenium.common.exceptions import TimeoutException

class ProfileJavascriptTest(StaticLiveServerTestCase):
    """Unit tests of javascript in profile view."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_patient.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/other_parents.json',
        'peer_support/tests/fixtures/other_user_profiles.json'
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        cls.selenium = WebDriver(options=options)
        cls.selenium.maximize_window()
        cls.selenium.implicitly_wait(40)
        cls.wait = WebDriverWait(cls.selenium, 50)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_add_friend_sends_request(self):
        user = User.objects.get(username='@janedoe')
        second_user = User.objects.get(username='@petrapickles')
        user.first_login = False
        user.save()
        self.selenium.get(f'{self.live_server_url}/log_in/')
        try:
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_input.send_keys('@janedoe')
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Find Friends')]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/profile/@petrapickles/']"))).click()

            user_actions_dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, "user-actions-dropdown"))).click()

            friend_link = self.wait.until(EC.element_to_be_clickable((By.ID, "friend-link")))
            self.assertEqual("Add friend", friend_link.text)
            friend_link.click()
            user_actions_dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, "user-actions-dropdown")))
            user_actions_dropdown.click()
            self.wait.until(EC.text_to_be_present_in_element((By.ID, "friend-link"), "Request sent"))
            self.assertEqual("Request sent", friend_link.get_attribute("innerHTML"))

            friend_request = FriendRequest.objects.get(sender=user, receiver=second_user)
            content_type_id = ContentType.objects.get_for_model(FriendRequest).id
            self.assertTrue(Notification.objects.filter(content_type=content_type_id, object_id=friend_request.id).exists())
            Notification.objects.filter(content_type=content_type_id, object_id=friend_request.id).delete()
            friend_request.delete()

        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")

    def test_remove_friend(self):
        user = User.objects.get(username='@janedoe')
        second_user = User.objects.get(username='@petrapickles')
        user.friends.add(second_user)
        user.first_login = False
        user.save()

        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_input.send_keys('@janedoe')

            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')

            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]')))
            login_button.click()

            friends_list_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Friends list')]")))
            friends_list_button.click()

            second_user_profile_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/profile/@petrapickles/']")))
            second_user_profile_link.click()

            user_actions_dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, "user-actions-dropdown")))
            user_actions_dropdown.click()

            friend_link = self.wait.until(EC.element_to_be_clickable((By.ID, "friend-link")))
            self.assertEqual("Remove friend", friend_link.get_attribute("innerHTML"))
            friend_link.click()

            user_actions_dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, "user-actions-dropdown")))
            user_actions_dropdown.click()

            friend_link = self.wait.until(EC.presence_of_element_located((By.ID, "friend-link")))
            self.assertEqual("Add friend", friend_link.get_attribute("innerHTML"))
            
            self.assertNotIn(second_user, user.friends.all())
            self.assertNotIn(user, second_user.friends.all())
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")

    def test_block_user_reloads_page(self):

        user = User.objects.get(username='@janedoe')
        second_user = User.objects.get(username='@petrapickles')
        user.first_login = False
        user.save()

        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            username_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "username")))
            username_input.send_keys('@janedoe')
            password_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()

            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Find Friends')]"))).click()

            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/profile/@petrapickles/']"))).click()

            user_actions_dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, "user-actions-dropdown")))
            user_actions_dropdown.click()

            self.wait.until(EC.visibility_of_element_located((By.ID, "profile-content")))

            block_link = self.wait.until(EC.element_to_be_clickable((By.ID, "block-link")))
            self.assertEqual("Block this user", block_link.get_attribute("innerHTML"))
            block_link.click()

            self.wait.until(EC.visibility_of_element_located((By.ID, "user-is-blocked")))

            user_actions_dropdown = self.wait.until(EC.visibility_of_element_located((By.ID, "user-actions-dropdown")))
            user_actions_dropdown.click()

            block_link = self.wait.until(EC.element_to_be_clickable((By.ID, "block-link")))
            self.assertEqual("Unblock this user", block_link.get_attribute("innerHTML"))
            self.assertIn(second_user, user.blocked_users.all())
            user.blocked_users.remove(second_user)
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")
            
    def test_unblock_user_reloads_page(self):

        user = User.objects.get(username='@janedoe')
        second_user = User.objects.get(username='@petrapickles')
        user.blocked_users.add(second_user)
        user.first_login = False
        user.save()

        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            self.wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys('@janedoe')
            self.wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='user-account-dropdown']/span"))).click()
            
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Settings"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Other users"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='display-blocklist']"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/profile/@petrapickles/']"))).click()

            self.wait.until(EC.element_to_be_clickable((By.ID, "user-actions-dropdown"))).click()
            self.wait.until(EC.visibility_of_element_located((By.ID, "user-is-blocked")))

            block_link = self.wait.until(EC.element_to_be_clickable((By.ID, "block-link")))
            self.assertEqual("Unblock this user", block_link.get_attribute("innerHTML"))
            block_link.click()

            self.wait.until(EC.element_to_be_clickable((By.ID, "user-actions-dropdown"))).click()

            self.wait.until(EC.visibility_of_element_located((By.ID, "profile-content")))

            block_link = self.wait.until(EC.element_to_be_clickable((By.ID, "block-link")))
            self.assertEqual("Block this user", block_link.get_attribute("innerHTML"))
            
            user.refresh_from_db()
            self.assertNotIn(second_user, user.blocked_users.all())
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")
