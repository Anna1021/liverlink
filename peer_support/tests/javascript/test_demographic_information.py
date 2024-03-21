"""Unit test of javascript in demographic information view"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from peer_support.models import User

class DemographicInformationJavascriptTest(StaticLiveServerTestCase):
    """Unit test of javascript in demographic information view"""

    fixtures = [
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_mentor.json',
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
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(40)
        cls.wait = WebDriverWait(cls.selenium, 20)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_charts_visible(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        user = User.objects.get(username='@admin')
        user.first_login = False
        user.save()
        try:
            username_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "username")))
            username_input.send_keys('@admin')
            password_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Admin')]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.ID, "demographic-information"))).click()

            self.wait.until(EC.presence_of_element_located((By.ID, "barChartDataSelect")))
            self.wait.until(EC.presence_of_element_located((By.ID, "pieChartDataSelect")))

            bar_chart_dropdown = Select(self.selenium.find_element(By.ID, "barChartDataSelect"))
            pie_chart_dropdown = Select(self.selenium.find_element(By.ID, "pieChartDataSelect"))

            bar_chart_dropdown.select_by_value("user_age")
            pie_chart_dropdown.select_by_value("ethnicity")
        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while self.waiting for the question to be visible or interactable: {e}")

    def test_dynamic_locations(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/log_in/'))
        user = User.objects.get(username='@admin')
        user.first_login = False
        user.save()
        try:
            username_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "username")))
            username_input.send_keys('@admin')
            password_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_input.send_keys('Password123')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Admin')]"))).click()
            self.wait.until(EC.element_to_be_clickable((By.ID, "demographic-information"))).click()

            self.wait.until(EC.presence_of_element_located((By.ID, "barChartDataSelect")))
            self.wait.until(EC.presence_of_element_located((By.ID, "pieChartDataSelect")))

            bar_chart_dropdown = Select(self.selenium.find_element(By.ID, "barChartDataSelect"))
            pie_chart_dropdown = Select(self.selenium.find_element(By.ID, "pieChartDataSelect"))

            bar_chart_dropdown.select_by_value("user_location")
            pie_chart_dropdown.select_by_value("user_location")

            self.wait.until(EC.presence_of_element_located((By.ID, "continentSelectBar")))
            self.wait.until(EC.presence_of_element_located((By.ID, "continentSelectPie")))

            bar_chart_location_dropdown = Select(self.selenium.find_element(By.ID, "continentSelectBar"))
            pie_chart_location_dropdown = Select(self.selenium.find_element(By.ID, "continentSelectPie"))

            bar_chart_location_dropdown.select_by_value("europe")
            pie_chart_location_dropdown.select_by_value("europe")

        except TimeoutException as e:
            self.fail(f"Test failed due to timeout while self.waiting for the question to be visible or interactable: {e}")