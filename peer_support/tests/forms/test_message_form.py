"""Unit tests of the message form."""
from django.test import TestCase
from peer_support.forms import MessageForm
from peer_support.models import User, Message, Conversation

class MessageFormTestCase(TestCase):
    """Unit tests of the message form."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_conversation.json',
        'peer_support/tests/fixtures/default_group_conversation.json',
        'peer_support/tests/fixtures/default_message.json',
        'peer_support/tests/fixtures/other_messages.json',
    ]

    def setUp(self):
        self.sender = User.objects.get(username='@johndoe')
        self.sender.conversations.set([1,2])
        self.receiver = User.objects.get(username='@janedoe')
        self.receiver.conversations.set([1])
        self.form_input = {'content':"Ploof"}
        self.conversation = Conversation.objects.get(pk=1)

    def test_form_has_necessary_fields(self):
        form = MessageForm(self.conversation)
        self.assertIn('content', form.fields)

    def test_valid_message_form(self):
        form = MessageForm(self.conversation, user=self.sender,data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_uses_model_validation(self):
        self.form_input['content'] = 'a'*101
        form = MessageForm(self.conversation, user=self.sender,data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = MessageForm(self.conversation, user = self.sender, data=self.form_input)
        before_count = Message.objects.count()
        form.save()
        after_count = Message.objects.count()
        self.assertEqual(after_count, before_count+1)
        message = Message.objects.last()
        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.content,"Ploof")

    def test_message_is_sent_to_conversation(self):
        messages_before = self.conversation.messages.count()
        form = MessageForm(self.conversation, user = self.sender, data=self.form_input)
        form.save()
        messages_after = self.conversation.messages.count()
        self.assertEqual(messages_after, messages_before+1)
        message = Message.objects.last()
        self.assertIn(message,self.conversation.messages.all())

    def test_previous_message_set_to_last_message(self):
        target_message = self.conversation.messages.last()
        form = MessageForm(self.conversation, user = self.sender, data=self.form_input)
        message = form.save()
        self.assertEqual(message.previous_message, target_message)

    def test_previous_message_none_if_no_messages_before(self):
        self.conversation.messages.set(Message.objects.none())
        form = MessageForm(self.conversation,user = self.sender, data=self.form_input)
        message = form.save()
        self.assertIsNone(message.previous_message)

    def test_deleted_conversation_returns_after_message_sent(self):
        users = User.objects.filter(username=self.receiver.username)
        self.assertIn(self.receiver, self.conversation.users.all())
        self.assertIn(self.conversation, self.receiver.conversations.all())
        self.conversation.delete(users)
        self.assertIn(self.receiver, self.conversation.users.all())
        self.assertNotIn(self.conversation, self.receiver.conversations.all())
        form = MessageForm(self.conversation, user = self.sender, data=self.form_input)
        message = form.save()
        self.assertIn(self.conversation, self.receiver.conversations.all())