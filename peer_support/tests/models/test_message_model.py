"""Unit tests for the Message model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from peer_support.models import User,Message

class UserModelTestCase(TestCase):
    """Unit tests for the Message model."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_message.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.message = Message.object.get(pk=1)

    def test_correct_sender(self):
        self.assertEqual(self.message.sender,self.user)

    def test_correct_contents(self):
        self.assertEqual(self.message.content,"Hello")

    def test_correct_read_status(self):
        self.assertFalse(self.message.read)