import uuid
from django.test import TestCase
from peer_support.models import Mentor, Referral
from peer_support.utils import create_referral, get_referral_code

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
