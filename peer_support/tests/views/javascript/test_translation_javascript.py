from selenium.common.exceptions import NoSuchElementException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LiveTranslationTest(StaticLiveServerTestCase):
    """Unit test of javascript which translates all views which contain navbar"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless")
        cls.selenium = WebDriver(service=Service(), options=options)
        cls.selenium.implicitly_wait(10)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_webpage_translates(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        
        # Checks translate widget is loaded
        try:
            translate_widget = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, "google_translate_element"))
            )
        except NoSuchElementException:
            self.fail("Google Translate widget not found on the page.")
        
