"""Unit tests of javascript in question page view."""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from peer_support.models import User, Question, Response

class QuestionPageJavascriptTest(StaticLiveServerTestCase):
    """Unit tests of javascript in question page view."""

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

    def test_hide_questions_and_responses_from_blocked_users(self):

        user = User.objects.get(username='@janedoe')
        blocked_user = User.objects.get(username='@peterpickles')
        user.blocked_users.add(blocked_user)

        #Create a question and response authored by @peterpickles
        question = Question.objects.create(author=blocked_user, title="Test title", body="This is the question body.")
        response = Response.objects.create(user=blocked_user, question=question, body="This is the response body.")

        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('@janedoe')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('Password123')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        self.selenium.find_element(By.XPATH, "//button[contains(text(), 'Resources')]").click()

        self.selenium.find_element(By.XPATH, "//p[@class='question-list-item-title' and contains(text(), 'Test title')]").click()

        hidden_question = self.selenium.find_element(By.ID, "blocked-question")
        self.assertEqual("You have blocked this user. Click to reveal question.", hidden_question.get_attribute("innerHTML"))
        self.assertIn("text-muted", hidden_question.get_attribute("class"))

        hidden_question.click()

        hidden_question = self.selenium.find_element(By.ID, "blocked-question")
        self.assertEqual(question.body, hidden_question.get_attribute("innerHTML"))
        self.assertNotIn("text-muted", hidden_question.get_attribute("class"))

        hidden_response = self.selenium.find_element(By.NAME, "blocked-response")
        self.assertEqual("You have blocked this user. Click to reveal response.", hidden_response.get_attribute("innerHTML"))
        self.assertIn("text-muted", hidden_response.get_attribute("class"))

        hidden_response.click()

        hidden_response = self.selenium.find_element(By.NAME, "blocked-response")
        self.assertEqual(response.body, hidden_response.get_attribute("innerHTML"))
        self.assertNotIn("text-muted", hidden_response.get_attribute("class"))