"""Unit test of javascript for font change."""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from peer_support.models import User
from selenium.webdriver.support.ui import Select


class FontChangeJavascriptTest(StaticLiveServerTestCase):
    """Unit test of javascript for font change."""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.selenium, 50)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_theme_switcher(self):
        user = User.objects.get(username='@johndoe')
        user.friends.set(User.objects.exclude(username='@johndoe'))
        user.first_login = False
        user.save()
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        try:
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_input.send_keys('@johndoe')
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='user-account-dropdown']/span"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Settings"))).click()
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Accessibility"))).click()
            main_div = self.wait.until(EC.presence_of_element_located((By.ID, "main-font")))
            self.assertIn('undefined', main_div.get_attribute('class'))
            font_family = main_div.value_of_css_property('font-family')
            expected_font='system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"'
            self.assertIn(expected_font, font_family)
            font_selector = main_div = self.wait.until(EC.presence_of_element_located((By.ID, "font-selector")))
            select = Select(font_selector)
            select.select_by_visible_text('Tahoma')
            font_family = main_div.value_of_css_property('font-family')
            self.assertIn('Tahoma', font_family)
            select.select_by_visible_text('Georgia')
            font_family = main_div.value_of_css_property('font-family')
            self.assertIn('Georgia', font_family)
            select.select_by_visible_text('Comic Sans')
            font_family = main_div.value_of_css_property('font-family')
            self.assertIn('Comic Sans MS', font_family)

        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")




