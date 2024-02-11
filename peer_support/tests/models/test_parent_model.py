"""Unit tests for the Parent model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from peer_support.models import Parent

class ParentModelTestCase(TestCase):
    """Unit tests for the Parent model."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users_parents.json',
        'peer_support/tests/fixtures/default_parent.json',
        'peer_support/tests/fixtures/other_parents.json'
    ]

    def setUp(self):
        self.parent = Parent.objects.get(username='@alexsmith')
        self.second_parent = Parent.objects.get(username='@sambennet')

    def test_valid_parent(self):
        self._assert_parent_is_valid()

    def test_child_condition_can_be_blank(self):
        self.parent.child_condition = ''
        self._assert_parent_is_valid()

    def test_child_condition_need_not_be_unique(self):
        self.parent.child_condition = self.second_parent.child_condition
        self._assert_parent_is_valid()

    def test_child_condition_can_be_100_characters_long(self):
        self.parent.child_condition = 'x' * 100
        self._assert_parent_is_valid()

    def test_child_condition_cannot_be_over_100_characters_long(self):
        self.parent.child_condition = 'x' * 101
        self._assert_parent_is_invalid()

    
    def test_child_age_of_diagnosis_can_be_blank(self):
        self.parent.child_age_of_diagnosis = None
        self._assert_parent_is_valid()

    def test_child_age_of_diagnosis_need_not_be_unique(self):
        self.parent.child_age_of_diagnosis = self.second_parent.child_age_of_diagnosis
        self._assert_parent_is_valid()

    def test_child_age_of_diagnosis_cannot_be_negative(self):
        self.parent.child_age_of_diagnosis = -1
        self._assert_parent_is_invalid()

    
    def _assert_parent_is_valid(self):
        try:
            self.parent.full_clean()
        except (ValidationError):
            self.fail('Test patient should be valid')

    def _assert_parent_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.parent.full_clean()