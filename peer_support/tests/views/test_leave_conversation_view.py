"""Tests for the leave conversation view"""
from django.test import TestCase
from django.urls import reverse
from peer_support.models import Message,Conversation,User
from django.contrib import messages

class DeleteMessageViewTestCase(TestCase):
    """Tests of the leave conversation view"""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/default_conversation.json',
                'peer_support/tests/fixtures/default_group_conversation.json',
                'peer_support/tests/fixtures/default_message.json'
    ]

    def setUp(self):
        self.conversation = Conversation.objects.get(pk=2)
        self.user = User.objects.get(username='@johndoe')
        self.user.conversations.set([1,2])
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('leave_conversation',kwargs={'conversation_id':self.conversation.id})

    def test_leave_conversation_url(self):
        self.assertEqual(self.url,'/leave_conversation/2')

    def test_successful_leave_group_conversation(self):
        self.assertIn(self.user,self.conversation.users.all())
        users_before = self.conversation.users.count()
        conversations_before = self.user.conversations.count()
        response = self.client.get(self.url,follow=True)
        self.assertNotIn(self.user,self.conversation.users.all())
        users_after = self.conversation.users.count()
        conversations_after = self.user.conversations.count()
        self.assertEqual(users_after,users_before-1)
        self.assertEqual(conversations_after,conversations_before - 1)
        redirect_url = reverse('conversation',kwargs={'conversation_id':0})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')

    def test_unsuccessful_leave_direct_conversation(self):
        self.conversation = Conversation.objects.get(pk=1)
        invalid_url = reverse('leave_conversation',kwargs={'conversation_id':1})
        self.assertIn(self.user,self.conversation.users.all())
        users_before = self.conversation.users.count()
        conversations_before = self.user.conversations.count()
        response = self.client.get(invalid_url,follow=True)
        self.assertIn(self.user,self.conversation.users.all())
        users_after = self.conversation.users.count()
        conversations_after = self.user.conversations.count()
        self.assertEqual(users_after,users_before)
        self.assertEqual(conversations_after,conversations_before)
        redirect_url = reverse('conversation',kwargs={'conversation_id':1})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')

    def test_unsuccessful_leave_nonexistent_conversation(self):
        invalid_url = reverse('leave_conversation',kwargs={'conversation_id':3})
        response = self.client.get(invalid_url,follow=True)
        redirect_url = reverse('conversation',kwargs={'conversation_id':0})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_unsuccessful_leave_conversation_user_is_not_in(self):
        self.client.logout()
        self.user = User.objects.get(username='@janedoe')
        self.client.login(username=self.user.username, password="Password123")
        invalid_url = reverse('leave_conversation',kwargs={'conversation_id':2})
        response = self.client.get(invalid_url,follow=True)
        redirect_url = reverse('conversation',kwargs={'conversation_id':0})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
