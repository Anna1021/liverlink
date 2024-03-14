"""Unit tests for the Professional model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from peer_support.models import Professional

class ProfessionalModelTestCase(TestCase):
    """Unit tests for the Professional model."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_professional.json',
        'peer_support/tests/fixtures/other_professionals.json'
    ]

    def setUp(self):
        self.professional = Professional.objects.get(username='@johndoe')

    def test_valid_professional(self):
        self._assert_professional_is_valid()

    def test_expertise_can_be_blank(self):
        self.professional.expertise = ''
        self._assert_professional_is_valid()

    def test_expertise_need_not_be_unique(self):
        second_professional = Professional.objects.get(username='@janedoe')
        self.professional.expertise = second_professional.expertise
        self._assert_professional_is_valid()

    def test_expertise_can_be_50_characters_long(self):
        self.professional.expertise = 'x' * 50
        self._assert_professional_is_valid()

    def test_expertise_cannot_be_over_50_characters_long(self):
        self.professional.expertise = 'x' * 51
        self._assert_professional_is_invalid()

    def test_professional_referral_code_cannot_be_blank(self):
        self.professional.referral_code = None
        self._assert_professional_is_invalid()
    
    def _assert_professional_is_valid(self):
        try:
            self.professional.full_clean()
        except (ValidationError):
            self.fail('Test professional should be valid')

    def _assert_professional_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.professional.full_clean()