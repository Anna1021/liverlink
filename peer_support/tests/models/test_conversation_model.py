"""Unit tests for the Conversation model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from peer_support.models import User,Message,Conversation

class ConversationModelTestCase(TestCase):
    """Unit tests for the Message model."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_message.json',
        'peer_support/tests/fixtures/other_messages.json',
        'peer_support/tests/fixtures/default_conversation.json',
        'peer_support/tests/fixtures/default_group_conversation.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.message = Message.objects.get(pk=1)
        self.conversation = Conversation.objects.get(pk=1)
        self.group_conversation = GroupConversation.objects.get(pk=2)

    def test_correct_group_size(self):
        self.assertEqual(self.conversation.users.count(),2)
        self.assertEqual(self.group_conversation2.users.count(),3)

    def test_correct_internal_group_name(self):
        self.assertIsNone(self.group_conversation.name)

    def test_correct_name_displayed(self):
        display1 = self.conversation1.display_name(self.user)
        display2 = self.conversation2.display_name(self.user)
        self.assertEqual(display1,"@janedoe")
        self.assertEqual(display2,"@johndoe, @peterpickles, @petrapickles")

    # def test_cannot_add_user_to_individual_chat(self):
    #     other_user=User.objects.get(pk=3)
    #     self.conversation1.add_user(other_user)
    #     self.assertEqual(self.conversation1.users.count(),2)

    def test_add_user_to_group(self):
        user2 = User.objects.get(pk=2)
        user3 = User.objects.get(pk=3)
        self.conversation2.add_user(user2)
        self.conversation3.add_user(user3)
        self.assertEqual(self.conversation2.users.count(),4)
        self.assertEqual(self.conversation3.users.count(),4)

    def test_adding_existing_user_has_no_effect(self):
        user2 = User.objects.get(pk=2)
        user3 = User.objects.get(pk=3)
        self.conversation2.add_user(user3)
        self.conversation3.add_user(user2)
        self.assertEqual(self.conversation2.users.count(),3)
        self.assertEqual(self.conversation3.users.count(),3)

    def test_sending_messages_adds_to_conversation(self):
        self.assertEqual(self.conversation1.messages.count(),1)
        new_message = Message.objects.get(pk=2)
        self.conversation1.send(new_message)
        self.assertEqual(self.conversation1.messages.count(),2)

    def test_sending_updates_non_sender_notifications(self):
        new_message = Message.objects.get(pk=2)
        other_user = User.objects.get(pk=2)
        self.assertNotIn(self.conversation1,other_user.unread_conversations.all())
        self.conversation1.send(new_message)
        self.assertIn(self.conversation1,other_user.unread_conversations.all())
        
    def test_sending_does_not_update_sender_notifications(self):
        new_message = Message.objects.get(pk=2)
        self.assertNotIn(self.conversation1,self.user.unread_conversations.all())
        self.conversation1.send(new_message)
        self.assertNotIn(self.conversation1,self.user.unread_conversations.all())

    

    
