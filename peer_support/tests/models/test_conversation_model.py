"""Unit tests for the Conversation model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from peer_support.models import User,Message,Conversation

class UserModelTestCase(TestCase):
    """Unit tests for the Message model."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_message.json',
        'peer_support/tests/fixtures/other_messages.json',
        'peer_support/tests/fixtures/default_conversation.json',
        'peer_support/tests/fixtures/other_conversations.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.message = Message.objects.get(pk=1)
        self.conversation1 = Conversation.objects.get(pk=1)
        self.conversation2 = Conversation.objects.get(pk=2)
        self.conversation3 = Conversation.objects.get(pk=3)

    def test_correct_group_size(self):
        self.assertEqual(self.conversation1.users.count(),2)
        self.assertEqual(self.conversation2.users.count(),3)
        self.assertEqual(self.conversation3.users.count(),3)

    def test_correct_internal_names(self):
        self.assertIsNone(self.conversation1.name)
        self.assertIsNone(self.conversation2.name)
        self.assertEqual(self.conversation3.name,"Test group")

    def test_correct_name_displayed(self):
        display1 = self.conversation1.display_name(self.user)
        display2 = self.conversation2.display_name(self.user)
        display3 = self.conversation3.display_name(self.user)
        self.assertEqual(display1,"@janedoe")
        self.assertEqual(display2,"@johndoe, @peterpickles, @petrapickles")
        self.assertEqual(display3,"Test group")

    
