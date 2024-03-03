"""Tests of the conversation creation view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.forms import ConversationForm, MessageForm
from peer_support.models import User, Conversation
                  
class ConversationViewTestCase(TestCase):
    """Tests of the conversation creation view."""

    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/default_conversation.json',
                'peer_support/tests/fixtures/default_group_conversation.json',
                'peer_support/tests/fixtures/default_message.json'
    ]

    def setUp(self):
        self.conversation = Conversation.objects.get(pk=1)
        self.url = reverse('create_conversation')
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password="Password123")
        self.user.friends.set(User.objects.exclude(pk=1))
        self.other_users = [2]

    def test_create_conversation_url(self):
        self.assertEqual(self.url,'/create_conversation/')

    def test_get_create_conversation(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_conversation.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ConversationForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_conversation_creation(self):
        form_input = {
            'users':[]
        }
        before_count = Conversation.objects.count()
        response = self.client.post(self.url,data=form_input)
        after_count = Conversation.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_conversation.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ConversationForm))
        self.assertTrue(form.is_bound)

    def test_successful_direct_conversation_creation(self):
        form_input = {
            'users':[3]
        }
        form = ConversationForm(self.user,data=form_input)
        self.assertTrue(form.is_valid())
        before_count = Conversation.objects.count()
        response = self.client.post(self.url, data=form_input,follow=True)
        after_count = Conversation.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertTemplateUsed(response, 'conversation.html')
        self.assertRedirects(response, reverse('conversation',kwargs={'conversation_id':3}), status_code=302, target_status_code=200)
        form = response.context['message_form']
        self.assertTrue(isinstance(form, MessageForm))
        self.assertFalse(form.is_bound)

    def test_successful_direct_conversation_retrieval(self):
        form_input = {
            'users':self.other_users
        }
        before_count = Conversation.objects.count()
        response = self.client.post(self.url, data=form_input,follow=True)
        after_count = Conversation.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'conversation.html')
        self.assertRedirects(response, reverse('conversation',kwargs={'conversation_id':1}), status_code=302, target_status_code=200)
        form = response.context['message_form']
        self.assertTrue(isinstance(form, MessageForm))
        self.assertFalse(form.is_bound)

    def test_successful_group_conversation_creation(self):
        form_input = {
            'users':self.other_users,
            'group':':3'
        }
        before_count = Conversation.objects.count()
        response = self.client.post(self.url, data=form_input,follow=True)
        after_count = Conversation.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertTemplateUsed(response, 'conversation.html')
        self.assertRedirects(response, reverse('conversation',kwargs={'conversation_id':3}), status_code=302, target_status_code=200)
        form = response.context['message_form']
        self.assertTrue(isinstance(form, MessageForm))
        self.assertFalse(form.is_bound)
