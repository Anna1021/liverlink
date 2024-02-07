"""Unit tests for the Conversation model."""
from django.test import TestCase
from peer_support.models import User,Message,Conversation

class ConversationModelTestCase(TestCase):
    """Unit tests for the Conversation model."""

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
        self.group_conversation = Conversation.objects.get(pk=2).as_group()

    def test_group_conversation_is_registered_as_group(self):
        self.assertIsNotNone(self.group_conversation)

    def test_conversation_is_not_registered_as_group(self):
        self.assertIsNone(self.conversation.as_group())

    def test_correct_group_size(self):
        self.assertEqual(self.conversation.users.count(),2)
        self.assertEqual(self.group_conversation.users.count(),3)

    def test_correct_internal_group_name(self):
        self.assertIsNone(self.group_conversation.name)

    

    def test_correct_group_name_displayed(self):
        display = self.group_conversation.display_name()
        self.assertEqual(display,"@johndoe, @peterpickles, @petrapickles")

    # def test_cannot_add_user_to_individual_chat(self):
    #     other_user=User.objects.get(pk=3)
    #     self.conversation.add_user(other_user)
    #     self.assertEqual(self.conversation.users.count(),2)

    def test_add_user_to_group(self):
        user2 = User.objects.get(pk=2)
        self.group_conversation.add_user(user2)
        self.assertEqual(self.group_conversation.users.count(),4)

    def test_adding_existing_user_has_no_effect(self):
        user = User.objects.get(pk=3)
        self.group_conversation.add_user(user)
        self.assertEqual(self.group_conversation.users.count(),3)

    def test_sending_messages_adds_to_conversation(self):
        self.assertEqual(self.conversation.messages.count(),1)
        new_message = Message.objects.get(pk=2)
        self.conversation.send(new_message)
        self.assertEqual(self.conversation.messages.count(),2)

    # def test_sending_updates_non_sender_notifications(self):
    #     new_message = Message.objects.get(pk=2)
    #     other_user = User.objects.get(pk=2)
    #     self.assertNotIn(self.conversation,other_user.unread_conversations.all())
    #     self.conversation.send(new_message)
    #     self.assertIn(self.conversation,other_user.unread_conversations.all())
        
    # def test_sending_does_not_update_sender_notifications(self):
    #     new_message = Message.objects.get(pk=2)
    #     self.assertNotIn(self.conversation,self.user.unread_conversations.all())
    #     self.conversation.send(new_message)
    #     self.assertNotIn(self.conversation,self.user.unread_conversations.all())

    

    
