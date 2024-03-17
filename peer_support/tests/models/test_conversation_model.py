"""Unit tests for the Conversation model."""
from django.test import TestCase
from peer_support.models import User, Message, Conversation

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
        self.user.conversations.set([1,2])
        self.other_user = User.objects.get(username='@janedoe')
        self.other_user.conversations.set([1])
        self.message = Message.objects.get(pk=1)
        self.conversation = Conversation.objects.get(pk=1)

    def test_conversation_is_not_registered_as_group(self):
        self.assertIsNone(self.conversation.as_group())

    def test_correct_group_size(self):
        self.assertEqual(self.conversation.users.count(), 2)

    def test_correct__name_displayed(self):
        display = str(self.conversation)
        self.assertEqual(display, "@janedoe, @johndoe")

    def test_sending_messages_adds_to_conversation(self):
        before_count = self.conversation.messages.count()
        new_message = Message.objects.create(
            sender=self.user,
            content='test',
            send_time="2024-01-20T10:00:00Z"
        )
        self.conversation.send(new_message)
        after_count = self.conversation.messages.count()
        self.assertEqual(after_count, before_count+1)

    def test_sending_messages_updates_last_updated(self):
        time_before = self.conversation.last_updated
        new_message = Message.objects.get(pk=2)
        self.conversation.send(new_message)
        self.assertNotEqual(time_before, self.conversation.last_updated)

    def test_conversation_still_exists_after_deleted_for_one(self):
        users_to_delete_message = self.conversation.users.filter(username=self.user.username)
        users_before = self.conversation.users.count()
        conversations_before = Conversation.objects.count()
        self.assertIn(self.conversation, self.user.conversations.all())
        self.message.delete(users_to_delete_message)
        conversations_after = Conversation.objects.count()
        users_after = self.conversation.users.count()
        self.assertEqual(users_after, users_before)
        self.assertEqual(conversations_after, conversations_before)

    def test_conversation_delete_for_all_at_once(self):
        before_count = Conversation.objects.count()
        self.conversation.delete(self.conversation.users.all())
        after_count = Conversation.objects.count()
        self.assertEqual(after_count, before_count-1)