from django.test import TestCase
from peer_support.models import Referral, Mentor
from django.db.utils import IntegrityError

class ReferralModelTestCase(TestCase):
    def setUp(self):
        self.referrer = Mentor.objects.create(name='John Doe', email='john@example.com')
        self.referral = Referral.objects.create(referrer=self.referrer, code='ABC123')

    def test_referral_creation(self):
        self.assertEqual(self.referral.code, 'ABC123')
        self.assertEqual(self.referral.referrer, self.referrer)

    def test_unique_code_constraint(self):
        with self.assertRaises(IntegrityError):
            Referral.objects.create(referrer=self.referrer, code='ABC123')  # Attempt to create a referral with the same code

    def test_referrer_referrals_relationship(self):
        self.assertEqual(self.referral.referrer, self.referrer)
        self.assertIn(self.referral, self.referrer.referrals_made.all())

    def test_max_length_code(self):
        referral = Referral.objects.create(referrer=self.referrer, code='A' * 20)
        self.assertEqual(len(referral.code), 20)

    def test_invalid_referrer(self):
        with self.assertRaises(TypeError):
            Referral.objects.create(referrer=None, code='XYZ456')
            