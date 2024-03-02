"""Tests of the conversation view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.forms import MessageForm
from peer_support.models import User, Conversation,Message
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
        self.conversation = Conversation.objects.get(pk=1)
        self.url = reverse('conversation',kwargs={'conversation_id':self.conversation.id})
        self.no_conversation_url = reverse('conversation',kwargs={'conversation_id':0})
        self.form_input = {
            'content':'Ploof'
        }
        self.user = User.objects.get(username='@janedoe')
        self.client.login(username=self.user.username, password="Password123")

    def test_conversation_url(self):
        self.assertEqual(self.url,'/conversation/1')

    def test_get_conversation(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversation.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, MessageForm))
        self.assertFalse(form.is_bound)
        blocked_dm = response.context['blocked_dm']
        self.assertFalse(blocked_dm)

    def test_get_direct_conversation_containing_blocked_user(self):
        blocked_user = User.objects.get(username='@johndoe')
        self.user.blocked_users.add(blocked_user)
        response = self.client.get(self.url)
        self.assertIsInstance(self.conversation, Conversation)
        self.assertIsNone(self.conversation.as_group())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversation.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, MessageForm))
        self.assertFalse(form.is_bound)
        blocked_dm = response.context['blocked_dm']
        self.assertTrue(blocked_dm)

    def test_cannot_get_conversation_user_is_not_in(self):
        invalid_url = reverse('conversation',kwargs={'conversation_id':2})
        response = self.client.get(invalid_url,follow=True)
        self.assertRedirects(response, self.no_conversation_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_cannot_get_conversation_that_does_not_exist(self):
        invalid_url = reverse('conversation',kwargs={'conversation_id':3})
        response = self.client.get(invalid_url,follow=True)
        self.assertRedirects(response, self.no_conversation_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_get_when_no_conversation_selected(self):
        response = self.client.get('/conversation/0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversation.html')

    def test_unsuccessful_message_send(self):
        self.form_input['content'] = ''
        before_count = Message.objects.count()
        response = self.client.post(self.url,data=self.form_input)
        after_count = Message.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversation.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, MessageForm))
        self.assertTrue(form.is_bound)

    def test_unsuccessful_direct_message_send_if_user_is_blocked(self):
        self.form_input['content'] = '123'
        blocked_user = User.objects.get(username='@johndoe')
        self.user.blocked_users.add(blocked_user)
        before_count = Message.objects.count()
        response = self.client.post(self.url,data=self.form_input)
        after_count = Message.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversation.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, MessageForm))
        self.assertTrue(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_successful_message_send(self):
        before_count = Message.objects.count()
        response = self.client.post(self.url, data=self.form_input)
        after_count = Message.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversation.html')
        message = Message.objects.get(pk=2)
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.content, 'Ploof')
        form = response.context['form']
        self.assertTrue(isinstance(form, MessageForm))
        self.assertFalse(form.is_bound)
