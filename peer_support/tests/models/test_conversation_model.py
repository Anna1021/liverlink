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

    def test_conversation_is_not_registered_as_group(self):
        self.assertIsNone(self.conversation.as_group())

    def test_correct_group_size(self):
        self.assertEqual(self.conversation.users.count(),2)

    def test_correct__name_displayed(self):
        display = str(self.conversation)
        self.assertEqual(display,"@janedoe, @johndoe")

    def test_sending_messages_adds_to_conversation(self):
        before_count = self.conversation.messages.count()
        new_message = Message.objects.create(
            sender=self.user,
            content='test',
            send_time="2024-01-20T10:00:00Z"
        )
        self.conversation.send(new_message)
        after_count = self.conversation.messages.count()
        self.assertEqual(after_count,before_count+1)

    def test_sending_messages_updates_last_updated(self):
        time_before = self.conversation.last_updated
        new_message = Message.objects.get(pk=2)
        self.conversation.send(new_message)
        self.assertNotEqual(time_before,self.conversation.last_updated)

    def test_conversation_delete(self):
        before_count = Conversation.objects.count()
        self.conversation.delete()
        after_count = Conversation.objects.count()
        self.assertEqual(after_count,before_count-1)

    def test_renaming_group_to_specific_name(self):
        new_name = 'Test'
        self.group_conversation.rename(new_name)
        self.assertEqual(self.group_conversation.name,'Test')

    def test_renaming_to_blank(self):
        new_name = ''
        self.group_conversation.rename(new_name)
        self.assertEqual(self.group_conversation.name,None)
    
    
    

    
