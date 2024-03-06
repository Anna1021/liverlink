"""Unit test of javascript theme switcher"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ThemeSwitcherTest(StaticLiveServerTestCase):
    """Unit test of javascript in theme switcher"""
    fixtures = ['peer_support/tests/fixtures/default_user.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless") 
        options.add_argument("--window-size=1920,1080")
        cls.selenium = WebDriver(service=Service(), options=options)
        cls.selenium.implicitly_wait(10)
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_theme_switcher(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('@johndoe')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('Password123')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        main_div = self.selenium.find_element(By.ID, "main")
        self.assertIn('dark-theme', main_div.get_attribute('class'))
        logo_image = self.selenium.find_element(By.CLASS_NAME, 'img-fluid')
        theme_logo_image = self.selenium.main_div = self.selenium.find_element(By.ID, "theme")
        self.assertEqual(theme_logo_image.get_attribute('class'), 'bi bi-sun')
        theme_logo_image.click() 
        WebDriverWait(self.selenium, 10).until(
            lambda driver: 'light-theme' in main_div.get_attribute('class')
        )
        self.assertEqual(logo_image.get_attribute('src'), self.live_server_url + '/static/images/Pulse-logo_black.png')
        self.assertEqual(theme_logo_image.get_attribute('class'), 'bi bi-moon-fill')
        # toggle back to the dark theme and verify changes
        theme_logo_image.click()
        WebDriverWait(self.selenium, 10).until(
            lambda driver: 'dark-theme' in main_div.get_attribute('class')
        )

        self.assertEqual(logo_image.get_attribute('src'), self.live_server_url + '/static/images/pulseLogoCropped.png')
        self.assertEqual(theme_logo_image.get_attribute('class'), 'bi bi-sun')