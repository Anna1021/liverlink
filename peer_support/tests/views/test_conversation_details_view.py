"""Tests of the conversation details view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.models import User, Conversation
from django.contrib import messages

class ConversationViewTestCase(TestCase):
    """Tests of the conversation view."""

    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/default_conversation.json',
                'peer_support/tests/fixtures/default_group_conversation.json',
                'peer_support/tests/fixtures/default_message.json'
    ]


    def setUp(self):
        self.conversation = Conversation.objects.get(pk=2)
        self.url = reverse('conversation_details',kwargs={'conversation_id':self.conversation.id})
        self.no_conversation_url = reverse('conversation',kwargs={'conversation_id':0})
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password="Password123")

    def test_conversation_url(self):
        self.assertEqual(self.url,'/conversation_details/2')

    def test_get_group_conversation_details(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversation_details.html')
        convo = response.context['conversation']
        self.assertEqual(convo,self.conversation.as_group())

    def test_cannot_get_direct_conversation(self):
        direct_conversation = Conversation.objects.get(id=1)
        invalid_url = reverse('conversation_details',kwargs={'conversation_id':direct_conversation.id})
        response = self.client.get(invalid_url,follow=True)
        target_url = reverse('conversation',kwargs={'conversation_id':direct_conversation.id})
        self.assertRedirects(response, target_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_cannot_get_conversation_user_is_not_in(self):
        self.client.logout()
        self.client.login(username='@janedoe',password='Password123')
        invalid_url = reverse('conversation_details',kwargs={'conversation_id':2})
        response = self.client.get(invalid_url,follow=True)
        self.assertRedirects(response, self.no_conversation_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_cannot_get_conversation_that_does_not_exist(self):
        invalid_url = reverse('conversation_details',kwargs={'conversation_id':3})
        response = self.client.get(invalid_url,follow=True)
        self.assertRedirects(response, self.no_conversation_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)