"""Tests for the message deletion view"""
from django.test import TestCase
from django.urls import reverse
from peer_support.models import Message,Conversation,User
from django.contrib import messages

class DeleteMessageViewTestCase(TestCase):
    """Tests of the message deletion view"""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/default_conversation.json',
                'peer_support/tests/fixtures/default_group_conversation.json',
                'peer_support/tests/fixtures/default_message.json',
                'peer_support/tests/fixtures/other_messages.json',
    ]

    def setUp(self):
        self.message = Message.objects.get(pk=1)
        self.conversation = Conversation.objects.get(pk=1)
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('delete_message',kwargs={'conversation_id':self.conversation.id,'message_id':self.message.id})

    def test_delete_message_url(self):
        self.assertEqual(self.url,'/delete_message/1/1/')

    def test_successful_delete_message_for_self(self):
        visible_to_before = self.message.visible_to.count()
        messages_before = Message.objects.count()
        response = self.client.get(self.url,follow=True)
        visible_to_after = self.message.visible_to.count()
        messages_after = Message.objects.count()
        self.assertEqual(visible_to_after,visible_to_before-1)
        self.assertEqual(messages_after,messages_before)
        redirect_url = reverse('conversation',kwargs={'conversation_id':self.conversation.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')

    def test_successful_delete_message_for_all_individually(self):
        visible_to_before = self.message.visible_to.count()
        messages_before = Message.objects.count()
        response = self.client.get(self.url,follow=True)
        self.client.logout()
        other_user = User.objects.get(username='@janedoe')
        self.client.login(username=other_user.username, password="Password123")
        response = self.client.get(self.url,follow=True)
        visible_to_after = self.message.visible_to.count()
        messages_after = Message.objects.count()
        self.assertEqual(visible_to_after,visible_to_before-2)
        self.assertEqual(messages_after,messages_before-1)
        redirect_url = reverse('conversation',kwargs={'conversation_id':self.conversation.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')

    def test_successful_delete_message_for_all_at_once(self):
        visible_to_before = self.message.visible_to.count()
        messages_before = Message.objects.count()
        response = self.client.get(self.url,follow=True,data={'delete_all':':3'})
        visible_to_after = self.message.visible_to.count()
        messages_after = Message.objects.count()
        self.assertEqual(visible_to_after,visible_to_before-2)
        self.assertEqual(messages_after,messages_before-1)
        redirect_url = reverse('conversation',kwargs={'conversation_id':self.conversation.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')

    def test_unsuccessful_delete_message_in_nonexistent_conversation(self):
        invalid_url = reverse('delete_message',kwargs={'conversation_id':3,'message_id':self.message.id})
        visible_to_before = self.message.visible_to.count()
        messages_before = Message.objects.count()
        response = self.client.get(invalid_url,follow=True)
        visible_to_after = self.message.visible_to.count()
        messages_after = Message.objects.count()
        self.assertEqual(visible_to_after,visible_to_before)
        self.assertEqual(messages_after,messages_before)
        redirect_url = reverse('conversation',kwargs={'conversation_id':0})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_unsuccessful_delete_message_in_conversation_user_is_not_in(self):
        other_user = self.user = User.objects.get(username='@janedoe')
        self.client.login(username=other_user.username, password="Password123")
        invalid_url = reverse('delete_message',kwargs={'conversation_id':2,'message_id':self.message.id})
        visible_to_before = self.message.visible_to.count()
        messages_before = Message.objects.count()
        response = self.client.get(invalid_url,follow=True)
        visible_to_after = self.message.visible_to.count()
        messages_after = Message.objects.count()
        self.assertEqual(visible_to_after,visible_to_before)
        self.assertEqual(messages_after,messages_before)
        redirect_url = reverse('conversation',kwargs={'conversation_id':0})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_unsuccessful_delete_message_not_in_conversation(self):
        invalid_url = reverse('delete_message',kwargs={'conversation_id':2,'message_id':self.message.id})
        visible_to_before = self.message.visible_to.count()
        messages_before = Message.objects.count()
        response = self.client.get(invalid_url,follow=True)
        visible_to_after = self.message.visible_to.count()
        messages_after = Message.objects.count()
        self.assertEqual(visible_to_after,visible_to_before)
        self.assertEqual(messages_after,messages_before)
        redirect_url = reverse('conversation',kwargs={'conversation_id':0})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_unsuccessful_delete_message_not_visible_to_user(self):
        self.client.get(self.url,follow=True)
        visible_to_before = self.message.visible_to.count()
        messages_before = Message.objects.count()
        response = self.client.get(self.url,follow=True)
        visible_to_after = self.message.visible_to.count()
        messages_after = Message.objects.count()
        self.assertEqual(visible_to_after,visible_to_before)
        self.assertEqual(messages_after,messages_before)
        redirect_url = reverse('conversation',kwargs={'conversation_id':0})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)