from django.urls import reverse
from with_asserts.mixin import AssertHTMLMixin
import uuid
from django.test import TestCase
from peer_support.models import Mentor, Referral
from peer_support.views.helpers import create_referral, get_referral_code


def reverse_with_next(url_name, next_url):
    """Extended version of reverse to generate URLs with redirects"""
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url


class LogInTester:
    """Class support login in tests."""
    def _is_logged_in(self):
        """Returns True if a user is logged in.  False otherwise."""
        return '_auth_user_id' in self.client.session.keys()

class MenuTesterMixin(AssertHTMLMixin):
    """Class to extend tests with tools to check the presents of menu items."""
    menu_urls = [reverse('profile'), reverse('log_out')]

    def assert_menu(self, response):
        """Check that menu is present."""
        for url in self.menu_urls:
            with self.assertHTML(response, f'a[href="{url}"]'):
                pass

    def assert_no_menu(self, response):
        """Check that no menu is present."""
        for url in self.menu_urls:
            self.assertNotHTML(response, f'a[href="{url}"]')

class UtilsTestCase(TestCase):
    """Unit tests for the util."""

    def setUp(self):
        self.mentor = Mentor.objects.create(username='test_mentor')
        
    def test_create_referral(self):
        referral = create_referral(self.mentor)
        self.assertIsInstance(referral, Referral)
        self.assertEqual(referral.referrer, self.mentor)
    
    def test_create_referral_invalid_user(self):
        invalid_user = 'invalid_user'
        referral = create_referral(invalid_user)
        self.assertIsNone(referral)

    def test_get_referral_code(self):
        code = uuid.uuid4().hex[:10].upper()
        Referral.objects.create(referrer=self.mentor, code=code)
        referral_code = get_referral_code(self.mentor)
        self.assertEqual(referral_code, code)

    def test_get_referral_code_no_referral(self):
        referral_code = get_referral_code(self.mentor)
        self.assertIsNone(referral_code)

    def tearDown(self):
        Mentor.objects.all().delete()
        Referral.objects.all().delete()
