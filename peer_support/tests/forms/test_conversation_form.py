"""Unit tests of the conversation form."""
from django import forms
from django.test import TestCase
from peer_support.forms import ConversationForm
from peer_support.models import User, Conversation

class MessageFormTestCase(TestCase):
    """Unit tests of the message form."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_conversation.json',
        'peer_support/tests/fixtures/default_group_conversation.json',
        'peer_support/tests/fixtures/default_message.json',
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.other_users = User.objects.exclude(pk=1)
        self.form_input = {
            'users' : self.other_users,
        }

    def test_form_has_necessary_fields(self):
        form = ConversationForm(self.user)
        self.assertIn('users', form.fields)

    def test_valid_user_form(self):
        form = ConversationForm(self.user,data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_must_save_correctly_for_group(self):
        form = ConversationForm(self.user,data=self.form_input)
        before_count = Conversation.objects.count()
        conversation = form.save(self.user,group=True)
        after_count = Conversation.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertEqual(conversation.id,3)
        self.assertIsNotNone(conversation.as_group())

    def test_form_retrieves_existing_conversation(self):
        self.form_input['users'] = User.objects.filter(pk=2)
        form = ConversationForm(self.user,data=self.form_input)
        before_count = Conversation.objects.count()
        conversation = form.save(self.user)
        after_count = Conversation.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(conversation.id,1)

    def test_form_must_save_correctly_for_direct_conversation(self):
        self.form_input['users'] = User.objects.filter(pk=3)
        form = ConversationForm(self.user,data=self.form_input)
        before_count = Conversation.objects.count()
        conversation = form.save(self.user)
        print(conversation.id)
        after_count = Conversation.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertEqual(conversation.id,3)