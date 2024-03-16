"""Tests for the delete conversation view"""
from django.test import TestCase
from django.urls import reverse
from peer_support.models import Conversation,User
from django.contrib import messages

class DeleteConversationViewTestCase(TestCase):
    """Tests of the delete conversation view"""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/default_conversation.json',
                'peer_support/tests/fixtures/default_group_conversation.json',
                'peer_support/tests/fixtures/default_message.json',
                'peer_support/tests/fixtures/other_messages.json',
    ]

    def setUp(self):
        self.conversation = Conversation.objects.get(pk=1)
        self.user = User.objects.get(username='@janedoe')
        self.user.conversations.set([1])
        self.client.force_login(self.user)
        self.url = reverse('delete_conversation', kwargs={'conversation_id':self.conversation.id})
        self.redirect_url = reverse('conversation', kwargs={'conversation_id':0})

    def test_leave_conversation_url(self):
        self.assertEqual(self.url,'/delete_conversation/1')

    def test_successful_delete_conversation(self):
        self.assertIn(self.user, self.conversation.users.all())
        users_before = self.conversation.users.count()
        conversations_before = self.user.conversations.count()
        response = self.client.get(self.url, follow=True)
        self.assertIn(self.user, self.conversation.users.all())
        users_after = self.conversation.users.count()
        conversations_after = self.user.conversations.count()
        self.assertEqual(users_after,users_before)
        self.assertEqual(conversations_after, conversations_before - 1)
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')

    def test_unsuccessful_delete_nonexistent_conversation(self):
        invalid_url = reverse('delete_conversation',kwargs={'conversation_id':3})
        response = self.client.get(invalid_url, follow=True)
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_unsuccessful_delete_conversation_user_is_not_in(self):
        invalid_url = reverse('delete_conversation',kwargs={'conversation_id':2})
        response = self.client.get(invalid_url, follow=True)
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_unsuccessful_delete_conversation_user_has_deleted(self):
        self.assertIn(self.conversation,self.user.conversations.all())
        self.assertIn(self.user, self.conversation.users.all())
        response = self.client.get(self.url,follow=True)
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertIn(self.user, self.conversation.users.all())
        self.assertNotIn(self.conversation, self.user.conversations.all())
        invalid_url = reverse('delete_conversation',kwargs={'conversation_id':2})
        response = self.client.get(invalid_url, follow=True)
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
