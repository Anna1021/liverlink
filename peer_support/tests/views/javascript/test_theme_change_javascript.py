"""Unit test of javascript theme switcher"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from peer_support.models import User

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
        cls.wait = WebDriverWait(cls.selenium, 50)
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_theme_switcher(self):
        user = User.objects.get(username='@johndoe')
        user.first_login = False
        user.save()
        self.selenium.get(f'{self.live_server_url}/log_in/')
        try:
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_input.send_keys('@johndoe')
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()

            main_div = self.wait.until(EC.presence_of_element_located((By.ID, "main")))
            self.assertIn('dark-theme', main_div.get_attribute('class'))
            logo_image = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "img-fluid")))

            theme_logo_image = self.wait.until(EC.presence_of_element_located((By.ID, "theme")))
            self.assertEqual(theme_logo_image.get_attribute('class'), 'bi bi-sun')

            theme_logo_image.click()

            self.wait.until(lambda driver: 'light-theme' in main_div.get_attribute('class'))

            self.assertEqual(logo_image.get_attribute('src'), self.live_server_url + '/static/images/Liver_Link_logo_black.png')
            self.assertEqual(theme_logo_image.get_attribute('class'), 'bi bi-moon-fill')
            theme_logo_image.click()
            self.wait.until(lambda driver: 'dark-theme' in main_div.get_attribute('class'))

            self.assertEqual(logo_image.get_attribute('src'), self.live_server_url + '/static/images/LiverLinkLogoCropped.png')
            self.assertEqual(theme_logo_image.get_attribute('class'), 'bi bi-sun')

        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while waiting for the question to be visible or interactable: {e}")
        

        main_div = self.selenium.find_element(By.ID, "main")
        self.assertIn('dark-theme', main_div.get_attribute('class'))
        logo_image = self.selenium.find_element(By.CLASS_NAME, 'img-fluid')
        theme_logo_image = self.selenium.main_div = self.selenium.find_element(By.ID, "theme")
        self.assertEqual(theme_logo_image.get_attribute('class'), 'bi bi-sun')
        theme_logo_image.click() 
        self.wait.until(
            lambda driver: 'light-theme' in main_div.get_attribute('class')
        )
        self.assertEqual(logo_image.get_attribute('src'), self.live_server_url + '/static/images/Liver_Link_logo_black.png')
        self.assertEqual(theme_logo_image.get_attribute('class'), 'bi bi-moon-fill')
        # toggle back to the dark theme and verify changes
        theme_logo_image.click()
        self.wait.until(
            lambda driver: 'dark-theme' in main_div.get_attribute('class')
        )

        self.assertEqual(logo_image.get_attribute('src'), self.live_server_url + '/static/images/LiverLinkLogoCropped.png')
        self.assertEqual(theme_logo_image.get_attribute('class'), 'bi bi-sun')