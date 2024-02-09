"""Unit tests for the Message model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from peer_support.models import User,Message

class MessageModelTestCase(TestCase):
    """Unit tests for the Message model."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_message.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.message = Message.objects.get(pk=1)

    def test_correct_sender(self):
        self.assertEqual(self.message.sender,self.user)

    def test_correct_contents(self):
        self.assertEqual(self.message.content,"Hello")

    def test_contents_must_have_at_least_one_character(self):
        self.message.content = ""
        self._assert_message_is_invalid()
        
    def _assert_message_is_valid(self):
        try:
            self.message.full_clean()
        except (ValidationError):
            self.fail('Message should be valid')

    def _assert_message_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.message.full_clean()

    