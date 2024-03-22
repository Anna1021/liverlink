"""Unit tests for the Feedback model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from peer_support.models import Feedback

class FeedbackModelTestCase(TestCase):
    """Tests for the Feedback model."""

    fixtures = [
        'peer_support/tests/fixtures/default_feedback.json',
    ]

    def setUp(self):
        self.feedback = Feedback.objects.get(id=1)

    def test_valid_feedback(self):
        self._assert_feedback_is_valid()


    def test_title_cannot_be_blank(self):
        self.feedback.title = ''
        self._assert_feedback_is_invalid()

    def test_title_can_be_50_characters_long(self):
        self.feedback.title = 'x' * 50
        self._assert_feedback_is_valid()

    def test_title_cannot_be_over_50_characters_long(self):
        self.feedback.title = 'x' * 51
        self._assert_feedback_is_invalid()


    def test_content_cannot_be_blank(self):
        self.feedback.content = ''
        self._assert_feedback_is_invalid()

    def test_content_can_be_500_characters_long(self):
        self.feedback.content = 'x' * 500
        self._assert_feedback_is_valid()

    def test_content_cannot_be_over_500_characters_long(self):
        self.feedback.content = 'x' * 501
        self._assert_feedback_is_invalid()


    def _assert_feedback_is_valid(self):
        try:
            self.feedback.full_clean()
        except (ValidationError):
            self.fail('Test feedback should be valid')

    def _assert_feedback_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.feedback.full_clean()