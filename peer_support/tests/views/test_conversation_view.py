"""Tests of the conversation view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.forms import MessageForm
from peer_support.models import User, Conversation,Message

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

    def test_unsuccessful_message_send(self):
        self.form_input['content'] = ''
        before_count = Message.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Message.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversation.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, MessageForm))
        self.assertTrue(form.is_bound)

    def test_successful_message_send(self):
        before_count = Message.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Message.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertRedirects(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        message = Message.objects.get(pk=2)
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.content, 'Ploof')
        form = response.context['form']
        self.assertTrue(isinstance(form, MessageForm))
        self.assertFalse(form.is_bound)
