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

    def test_message_still_exists_after_sender_deleted(self):
        before_count = Message.objects.count()
        User.objects.filter(username='@johndoe').delete()
        after_count = Message.objects.count()
        self.assertEqual(before_count,after_count)
        msg = Message.objects.get(pk=1)
        self.assertIsNone(msg.sender)
        
    def _assert_message_is_valid(self):
        try:
            self.message.full_clean()
        except (ValidationError):
            self.fail('Message should be valid')

    def _assert_message_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.message.full_clean()

    