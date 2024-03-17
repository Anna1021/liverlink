"""Unit tests of the add users form."""
from django.test import TestCase
from peer_support.forms import AddUsersForm
from peer_support.models import User, Conversation

class AddUsersFormTestCase(TestCase):
    """Unit tests of the add users form."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_conversation.json',
        'peer_support/tests/fixtures/default_group_conversation.json',
        'peer_support/tests/fixtures/default_message.json',
        'peer_support/tests/fixtures/other_messages.json',
    ]

    def setUp(self):
        self.conversation = Conversation.objects.get(pk=2)
        self.user = User.objects.get(pk=1)
        self.user_to_add = User.objects.filter(pk=2)
        self.form_input = {
            'users' : self.user_to_add,
        }
        self.user.friends.set(self.user_to_add)

    def test_form_has_necessary_fields(self):
        form = AddUsersForm(self.user, self.conversation)
        self.assertIn('users', form.fields)

    def test_valid_user_form(self):
        form = AddUsersForm(self.user, self.conversation, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_must_save_correctly(self):
        form = AddUsersForm(self.user, self.conversation, data=self.form_input)
        before_count = self.conversation.users.count()
        self.assertNotIn(self.user_to_add[0], self.conversation.users.all())
        form.save(self.conversation)
        after_count = self.conversation.users.count()
        self.assertEqual(after_count, before_count+1)
        self.assertIn(self.user_to_add[0], self.conversation.users.all())