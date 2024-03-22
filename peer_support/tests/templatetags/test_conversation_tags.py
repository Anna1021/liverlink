"""Unit tests for the conversation template tags"""
from peer_support.templatetags import conversation_tags
from django.test import TestCase
from peer_support.models import User, Conversation

class ConversationTagsTestCase(TestCase):
    """Unit tests for the conversation template tags"""

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
        self.conversation = Conversation.objects.get(pk=1)
        self.group_conversation = Conversation.objects.get(pk=2)

    def test_no_sender_for_same_sender(self):
        other_user = User.objects.get(username='@petrapickles')
        first_message = self.group_conversation.messages.filter(sender=self.user).all()[0]
        second_message = self.group_conversation.messages.filter(sender=self.user).all()[1]
        self.assertEqual(first_message.sender,second_message.sender)
        target_sender = ''
        actual_sender = conversation_tags.sender_if_applicable(second_message,other_user,self.group_conversation)
        self.assertEqual(target_sender,actual_sender)

    def test_no_senders_for_direct_conversation(self):
        message = self.conversation.messages.all()[0]
        target_sender = ''
        other_user = User.objects.get(username='@janedoe')
        actual_sender = conversation_tags.sender_if_applicable(message,other_user,self.conversation)
        self.assertEqual(target_sender,actual_sender)

    def test_sender_for_first_message(self):
        other_user = User.objects.get(username='@petrapickles')
        message = self.group_conversation.messages.all()[0]
        target_sender = '@johndoe'
        actual_sender = conversation_tags.sender_if_applicable(message,other_user,self.group_conversation)
        self.assertEqual(target_sender,actual_sender)
    
    def test_sender_for_different_sender(self):
        message = self.group_conversation.messages.all()[2]
        target_sender = '@petrapickles'
        actual_sender = conversation_tags.sender_if_applicable(message,self.user,self.group_conversation)
        self.assertEqual(target_sender,actual_sender)

    def test_sender_updates_if_previous_with_same_sender_deleted(self):
        other_user = User.objects.get(username='@petrapickles')
        first_message = self.group_conversation.messages.all()[0]
        second_message = self.group_conversation.messages.all()[1]
        target_sender = ''
        actual_sender = conversation_tags.sender_if_applicable(second_message,other_user,self.group_conversation)
        self.assertEqual(target_sender,actual_sender)
        first_message.delete([other_user])
        second_message = self.group_conversation.messages.all()[1]
        target_sender = '@johndoe'
        actual_sender = conversation_tags.sender_if_applicable(second_message,other_user,self.group_conversation)
        self.assertEqual(target_sender,actual_sender)

    def test_correct_direct_conversation_names(self):
        current_user = self.conversation.get_first_member()
        target_name = self.conversation.get_second_member().username
        actual_name = conversation_tags.conversation_name(current_user,self.conversation)
        self.assertEqual(target_name,actual_name)
        current_user = self.conversation.get_second_member()
        target_name = self.conversation.get_first_member().username
        actual_name = conversation_tags.conversation_name(current_user,self.conversation)
        self.assertEqual(target_name,actual_name)

    def test_correct_group_conversation_name(self):
        target_name = str(self.group_conversation.as_group())
        actual_name = conversation_tags.conversation_name(self.user,self.group_conversation)
        self.assertEqual(target_name,actual_name)


