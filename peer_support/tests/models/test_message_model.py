"""Unit tests for the Message model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from peer_support.models import User,Message, Conversation

class MessageModelTestCase(TestCase):
    """Unit tests for the Message model."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_message.json',
        'peer_support/tests/fixtures/other_messages.json',
        'peer_support/tests/fixtures/default_conversation.json',
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

    def test_message_deleted_after_conversation_deleted(self):
        conversation = Conversation.objects.get(pk=1)
        number_messages_in_conversation = conversation.messages.count()
        before_count = Message.objects.count()
        conversation.delete()
        after_count = Message.objects.count()
        self.assertEqual(after_count,before_count-number_messages_in_conversation)

    def test_message_still_exists_after_deleted_for_all_but_one(self):
        conversation = Conversation.objects.get(pk=1)
        users_to_delete_message = conversation.users.exclude(username=self.user.username)
        visible_before = self.message.visible_to.count()
        self.assertEqual(visible_before,conversation.users.count())
        messages_before = Message.objects.count()
        self.message.delete(users_to_delete_message)
        messages_after = Message.objects.count()
        self.assertEqual(messages_after,messages_before)
        self.assertEqual(self.message.visible_to.count(),1)

    def test_message_removed_when_deleted_for_all(self):
        conversation = Conversation.objects.get(pk=1)
        users_to_delete_message = conversation.users.all()
        visible_before = self.message.visible_to.count()
        self.assertEqual(visible_before,conversation.users.count())
        messages_before = Message.objects.count()
        self.message.delete(users_to_delete_message)
        messages_after = Message.objects.count()
        self.assertEqual(messages_after,messages_before-1)

    def test_previous_message_none_when_previous_message_deleted(self):
        conversation = Conversation.objects.get(pk=1)
        users_to_delete_message = conversation.users.all()
        message_before = Message.objects.get(pk=4)
        self.assertEqual(message_before.previous_message,self.message)
        self.message.delete(users_to_delete_message)
        message_after = Message.objects.get(pk=4)
        self.assertIsNone(message_after.previous_message)
        
    def _assert_message_is_valid(self):
        try:
            self.message.full_clean()
        except (ValidationError):
            self.fail('Message should be valid')

    def _assert_message_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.message.full_clean()

    