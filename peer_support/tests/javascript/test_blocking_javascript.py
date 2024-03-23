"""Unit tests of javascript for hiding content from blocked users."""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from peer_support.models import User, Conversation, Message, Question, Response, Post, PostComment

class BlockingJavascriptTest(StaticLiveServerTestCase):
    """Unit tests of javascript for hiding content from blocked users."""

    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        cls.selenium = WebDriver(options=options)
        cls.selenium.maximize_window()
        cls.selenium.implicitly_wait(40)
        cls.wait = WebDriverWait(cls.selenium, 20)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_hide_messages_from_blocked_users(self):
        user = User.objects.get(username='@johndoe')
        blocked_user = User.objects.get(username='@janedoe')
        user.blocked_users.add(blocked_user)
        user.first_login = False
        user.save()

        conversation = Conversation.objects.create()
        message = Message.objects.create(sender=blocked_user, content='ABC')
        message.visible_to.add(user)
        conversation.messages.add(message)
        conversation.users.add(user)
        conversation.users.add(blocked_user)
        user.conversations.add(conversation)

        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            self.wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys('@johndoe')
            self.wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()

            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Messages')]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "@janedoe"))).click()

            css_selector = "div.text-muted[data-blocked='true']"

            hidden_message = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            self.assertEqual("You have blocked this user. Click to reveal text.", hidden_message.get_attribute("innerHTML"))
            self.assertIn("text-muted", hidden_message.get_attribute("class"))

            hidden_message.click()

            self.assertEqual(message.content, hidden_message.get_attribute("innerHTML"))
            self.assertNotIn("text-muted", hidden_message.get_attribute("class"))

        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")

    def test_hide_questions_and_responses_from_blocked_users(self):
        user = User.objects.get(username='@janedoe')
        blocked_user = User.objects.get(username='@peterpickles')
        user.blocked_users.add(blocked_user)
        user.first_login = False
        user.save()
        question = Question.objects.create(author=blocked_user, title="Test title", body="This is the question body.")
        response = Response.objects.create(user=blocked_user, question=question, body="This is the response body.")
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            self.wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys('@janedoe')
            self.wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()

            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Resources')]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='question-list-item-title' and contains(text(), 'Test title')]"))).click()

            css_selector = "p.text-muted[data-blocked='true']"

            hidden_question = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            self.assertEqual("You have blocked this user. Click to reveal text.", hidden_question.get_attribute("innerHTML"))
            self.assertIn("text-muted", hidden_question.get_attribute("class"))

            hidden_question.click()

            self.assertEqual(question.body, hidden_question.get_attribute("innerHTML"))
            self.assertNotIn("text-muted", hidden_question.get_attribute("class"))

            hidden_response =self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
            self.assertEqual("You have blocked this user. Click to reveal text.", hidden_response.get_attribute("innerHTML"))
            self.assertIn("text-muted", hidden_response.get_attribute("class"))

            hidden_response.click()
            self.assertEqual(response.body, hidden_response.get_attribute("innerHTML"))
            self.assertNotIn("text-muted", hidden_response.get_attribute("class"))
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")

    def test_hide_post_comments_from_blocked_users(self):
        user = User.objects.get(username='@janedoe')
        blocked_user = User.objects.get(username='@peterpickles')
        user.blocked_users.add(blocked_user)
        user.first_login = False
        user.save()
        post = Post.objects.create(author=user, content="This is the post content.")
        comment = PostComment.objects.create(author=blocked_user, post=post, content="This is the comment content.")
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            self.wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys('@janedoe')
            self.wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()

            self.wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "This is the post content."))).click()

            css_selector = "p.text-muted[data-blocked='true']"

            hidden_comment = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            self.assertEqual("You have blocked this user. Click to reveal text.", hidden_comment.get_attribute("innerHTML"))
            self.assertIn("text-muted", hidden_comment.get_attribute("class"))

            hidden_comment.click()

            self.assertEqual(comment.content, hidden_comment.get_attribute("innerHTML"))
            self.assertNotIn("text-muted", hidden_comment.get_attribute("class"))
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")


