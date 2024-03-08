"""Tests of the get conversation view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User, Conversation, GroupConversation

class GetConversationViewTestCase(TestCase):
    """Tests of the get conversation view."""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',]

    def setUp(self):
        self.url = reverse('get_conversation', args=[2])
        self.user = User.objects.get(username='@johndoe')
        self.second_user = User.objects.get(username='@janedoe')
        self.client.login(username=self.user.username, password='Password123')

    def test_get_conversation_url(self):
        self.assertEqual(self.url, '/get_conversation/2')

    def test_get_conversation_when_no_conversation_exists(self):
        self.assertEqual(Conversation.objects.count(), 0)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Conversation.objects.count(), 1)
        conversation = Conversation.objects.first()
        redirect_url = reverse('conversation', kwargs={'conversation_id': conversation.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertIn(self.user, conversation.users.all())
        self.assertIn(self.second_user, conversation.users.all())
        self.assertEqual(2, conversation.users.count())
        self.assertIsNone(conversation.as_group())
        self.assertIn(conversation, self.user.conversations.all())
        self.assertIn(conversation, self.second_user.conversations.all())

    def test_get_conversation_when_no_direct_conversation_exists(self):
        groupchat = GroupConversation.objects.create()
        groupchat.users.add(self.user)
        groupchat.users.add(self.second_user)
        self.assertIsNotNone(groupchat.as_group())
        self.assertEqual(Conversation.objects.count(), 1)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Conversation.objects.count(), 2)
        conversation = Conversation.objects.last()
        redirect_url = reverse('conversation', kwargs={'conversation_id': conversation.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertNotEqual(groupchat, conversation)
        self.assertIn(self.user, conversation.users.all())
        self.assertIn(self.second_user, conversation.users.all())
        self.assertEqual(2, conversation.users.count())
        self.assertIsNone(conversation.as_group())
        self.assertIn(conversation, self.user.conversations.all())
        self.assertIn(conversation, self.second_user.conversations.all())

    def test_get_conversation_when_conversation_exists(self):
        conv = Conversation.objects.create()
        conv.users.add(self.user)
        conv.users.add(self.second_user)
        self.user.conversations.add(conv)
        self.second_user.conversations.add(conv)
        self.assertIsNone(conv.as_group())
        self.assertEqual(Conversation.objects.count(), 1)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Conversation.objects.count(), 1)
        conversation = Conversation.objects.first()
        redirect_url = reverse('conversation', kwargs={'conversation_id': conversation.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertEqual(conv, conversation)
        self.assertIn(self.user, conversation.users.all())
        self.assertIn(self.second_user, conversation.users.all())
        self.assertEqual(2, conversation.users.count())
        self.assertIsNone(conversation.as_group())
        self.assertIn(conversation, self.user.conversations.all())
        self.assertIn(conversation, self.second_user.conversations.all())

    def test_get_conversation_without_being_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
