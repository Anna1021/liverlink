"""Unit tests for the Group Conversation model."""
from django.test import TestCase
from peer_support.models import User,Message,Conversation

class GroupConversationModelTestCase(TestCase):
    """Unit tests for the Group Conversation model."""

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
        self.group_conversation = Conversation.objects.get(pk=2).as_group()

    def test_group_conversation_is_registered_as_group(self):
        self.assertIsNotNone(self.group_conversation)

    def test_correct_group_size(self):
        self.assertEqual(self.group_conversation.users.count(),3)

    def test_correct_internal_group_name(self):
        self.assertIsNone(self.group_conversation.name)

    def test_correct_unset_group_names_displayed(self):
        display = str(self.group_conversation)
        self.assertEqual(display,"@johndoe, @peterpickles, @petrapickles")
        display_name = self.group_conversation.display_name()
        self.assertEqual(display_name,"")

    def test_correct_set_group_names_displayed(self):
        self.group_conversation.name = 'test'
        display = str(self.group_conversation)
        self.assertEqual(display,"test")
        display_name = self.group_conversation.display_name()
        self.assertEqual(display_name,"test")

    def test_add_user_to_group(self):
        user2 = User.objects.filter(pk=2)
        self.group_conversation.add_users(user2)
        self.assertEqual(self.group_conversation.users.count(),4)

    def test_adding_existing_user_has_no_effect(self):
        user = User.objects.filter(pk=3)
        self.group_conversation.add_users(user)
        self.assertEqual(self.group_conversation.users.count(),3)

    def test_sending_messages_adds_to_conversation(self):
        before_count = self.group_conversation.messages.count()
        new_message = Message.objects.create(
            sender=self.user,
            content='test',
            send_time="2024-01-20T10:00:00Z"
        )
        self.conversation.send(new_message)
        after_count = self.group_conversation.messages.count()
        self.assertEqual(after_count,before_count+1)

    def test_sending_messages_updates_last_updated(self):
        time_before = self.group_conversation.last_updated
        new_message = Message.objects.get(pk=2)
        self.conversation.send(new_message)
        self.assertNotEqual(time_before,self.group_conversation.last_updated)

    def test_user_not_in_group_when_user_deleted(self):
        self.assertIn(self.user,self.group_conversation.users.all())
        User.objects.filter(username='@johndoe').delete()
        self.assertNotIn(self.user,self.group_conversation.users.all())

    def test_conversation_deleted_when_user_list_empty(self):
        before_count = Conversation.objects.count()
        for user in self.group_conversation.users.all():
            self.group_conversation.remove_user(user)
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
    
    
    

    