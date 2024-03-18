"""Unit tests of javascript in question page view."""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from peer_support.models import User, Question, Response
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class QuestionPageJavascriptTest(StaticLiveServerTestCase):
    """Unit tests of javascript in question page view."""

    fixtures = ['peer_support/tests/fixtures/other_users.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--window-size=1920,1080")
        cls.selenium = WebDriver(options=options)
        cls.selenium.maximize_window()
        cls.selenium.implicitly_wait(40)
        cls.wait = WebDriverWait(cls.selenium, 20)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

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

            hidden_question =self.wait.until(EC.visibility_of_element_located((By.ID, "blocked-question")))
            self.assertEqual("You have blocked this user. Click to reveal question.", hidden_question.get_attribute("innerHTML"))
            self.assertIn("text-muted", hidden_question.get_attribute("class"))

            hidden_question.click()

            hidden_question =self.wait.until(EC.visibility_of_element_located((By.ID, "blocked-question")))
            self.assertEqual(question.body, hidden_question.get_attribute("innerHTML"))
            self.assertNotIn("text-muted", hidden_question.get_attribute("class"))

            hidden_response =self.wait.until(EC.visibility_of_element_located((By.NAME, "blocked-response")))
            self.assertEqual("You have blocked this user. Click to reveal response.", hidden_response.get_attribute("innerHTML"))
            self.assertIn("text-muted", hidden_response.get_attribute("class"))

            hidden_response.click()

            hidden_response =self.wait.until(EC.visibility_of_element_located((By.NAME, "blocked-response")))
            self.assertEqual(response.body, hidden_response.get_attribute("innerHTML"))
            self.assertNotIn("text-muted", hidden_response.get_attribute("class"))
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")

