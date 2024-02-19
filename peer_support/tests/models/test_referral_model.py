"""Unit tests for the Referral model."""
from django.test import TestCase
from peer_support.models import Referral, Mentor
from django.core.exceptions import ValidationError

class ReferralModelTestCase(TestCase):
    def setUp(self):
        self.referrer = Mentor.objects.create(username='@johndoe')
        self.referral = Referral.objects.create(referrer=self.referrer, code='ABC123')

    def test_valid_referrer(self):
        self._assert_referral_is_valid()

    def test_unique_code_constraint(self):
        second_referral = Referral.objects.create(referrer=self.referrer, code='ABC123')
        self._assert_referral_is_invalid()

    def test_max_length_code(self):
        self.referral.code ='A' * 20
        self._assert_referral_is_invalid()

    def test_invalid_referrer(self):
        referrer = Referral.objects.create(referrer=None, code='XYZ456')
        self._assert_referral_is_invalid()

    def _assert_referral_is_valid(self):
        try:
            self.referral.full_clean()
        except (ValidationError):
            self.fail('Test referral should be valid')

    def _assert_referral_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.referral.full_clean()
