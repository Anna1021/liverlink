"""Unit tests for the Mentor model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from peer_support.models import Mentor

class MentorModelTestCase(TestCase):
    """Unit tests for the Mentor model."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_mentor.json',
        'peer_support/tests/fixtures/other_mentors.json'
    ]

    def setUp(self):
        self.mentor = Mentor.objects.get(username='@lindajohnson')
        self.second_mentor = Mentor.objects.get(username='@carlosmartinez')

    def test_valid_mentor(self):
        self._assert_mentor_is_valid()

    def test_condition_can_be_blank(self):
        self.mentor.condition = ''
        self._assert_mentor_is_valid()

    def test_condition_need_not_be_unique(self):
        self.mentor.condition = self.second_mentor.condition
        self._assert_mentor_is_valid()

    def test_condition_can_be_100_characters_long(self):
        self.mentor.condition = 'x' * 100
        self._assert_mentor_is_valid()

    def test_condition_cannot_be_over_100_characters_long(self):
        self.mentor.condition = 'x' * 101
        self._assert_mentor_is_invalid()
    
    def test_age_of_diagnosis_can_be_blank(self):
        self.mentor.age_of_diagnosis = None
        self._assert_mentor_is_valid()

    def test_age_of_diagnosis_need_not_be_unique(self):
        self.mentor.age_of_diagnosis = self.second_mentor.age_of_diagnosis
        self._assert_mentor_is_valid()

    def test_age_of_diagnosis_cannot_be_negative(self):
        self.mentor.age_of_diagnosis = -1
        self._assert_mentor_is_invalid()

    def test_mentor_referral_code_cannot_be_blank(self):
        self.mentor.referral_code = None
        self._assert_mentor_is_invalid()
    
    def _assert_mentor_is_valid(self):
        try:
            self.mentor.full_clean()
        except (ValidationError):
            self.fail('Test mentor should be valid')

    def _assert_mentor_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.mentor.full_clean()