"""Unit tests of reporting javascript."""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from peer_support.models import User,  Report, Post
from selenium.common.exceptions import TimeoutException
from django.contrib.contenttypes.models import ContentType

class ReportingJavascriptTest(StaticLiveServerTestCase):
    """Unit tests of reporting javascript."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_patient.json',
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_post.json',]

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

    def test_reported_object_muted(self):
        self.user = User.objects.get(username='@admin')
        post_content_type = ContentType.objects.get_for_model(Post)
        self.report_post = Report.objects.create(
            reporter=self.user,
            reason="other",
            content_type=post_content_type,
            object_id=Post.objects.first().pk
        )
        self.user.first_login = False
        self.user.save()
        self.selenium.get(f'{self.live_server_url}/log_in/')
        try:
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_input.send_keys('@admin')
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.selenium.get(f'{self.live_server_url}/post/1/')
            css_selector = "h6.text-muted[data-reported='true']"

            located_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            self.assertEqual("You have reported this. Click to reveal.", located_element.get_attribute("innerHTML"))
            self.assertEqual("text-muted", located_element.get_attribute("class"))
            located_element.click()
            self.assertEqual(located_element.get_attribute("data-text"), located_element.get_attribute("innerHTML"))
            self.assertEqual("", located_element.get_attribute("class"))

        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")