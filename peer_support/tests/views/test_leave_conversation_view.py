"""Tests for the leave conversation view"""
from django.test import TestCase
from django.urls import reverse
from peer_support.models import Message,Conversation,User

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
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('leave',kwargs={'conversation_id':self.conversation.id})

    def test_delete_message_url(self):
        self.assertEqual(self.url,'/leave_conversation/')

    def test_successful_leave_group_conversation(self):
        self.assertIn(self.user,self.conversation.users.all())
        users_before = self.conversation.users.count()
        conversations_before = self.user.conversations.count()
        response = self.client.get(self.url,follow=True)
        users_after = self.conversation.users.count()
        conversations_after = self.user.conversations.count()
        self.assertEqual(visible_to_after,visible_to_before-1)
        self.assertEqual(messages_after,messages_before)
        redirect_url = reverse('conversation',kwargs={'conversation_id':0})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
