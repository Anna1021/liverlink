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
        self.mentor = Mentor.objects.get(username='@johndoe')

    def test_valid_mentor(self):
        self._assert_mentor_is_valid()

    def test_mentor_condition_can_be_blank(self):
        self.mentor.mentor_condition = ''
        self._assert_mentor_is_valid()

    def test_mentor_condition_need_not_be_unique(self):
        second_mentor = Mentor.objects.get(username='@janedoe')
        self.mentor.mentor_condition = second_mentor.mentor_condition
        self._assert_mentor_is_valid()

    def test_mentor_condition_can_be_50_characters_long(self):
        self.mentor.mentor_condition = 'x' * 50
        self._assert_mentor_is_valid()

    def test_mentor_condition_cannot_be_over_50_characters_long(self):
        self.mentor.mentor_condition = 'x' * 51
        self._assert_mentor_is_invalid()
    
    def test_mentor_age_of_diagnosis_can_be_blank(self):
        self.mentor.mentor_age_of_diagnosis = None
        self._assert_mentor_is_valid()

    def test_mentor_age_of_diagnosis_need_not_be_unique(self):
        second_mentor = Mentor.objects.get(username='@janedoe')
        self.mentor.mentor_age_of_diagnosis = second_mentor.mentor_age_of_diagnosis
        self._assert_mentor_is_valid()

    def test_mentor_age_of_diagnosis_cannot_be_negative(self):
        self.mentor.mentor_age_of_diagnosis = -1
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