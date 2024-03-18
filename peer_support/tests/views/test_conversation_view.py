"""Tests of the conversation view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.forms import MessageForm, ReportForm
from peer_support.models import User, Conversation,Message, Report
from django.contrib import messages

class ConversationViewTestCase(TestCase):
    """Tests of the conversation view."""

    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/default_conversation.json',
                'peer_support/tests/fixtures/default_group_conversation.json',
                'peer_support/tests/fixtures/default_message.json',
                'peer_support/tests/fixtures/other_messages.json',
    ]

    def setUp(self):
        self.conversation = Conversation.objects.get(pk=1)
        self.message = Message.objects.get(pk=1)
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
        form = response.context['message_form']
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
        form = response.context['message_form']
        self.assertTrue(isinstance(form, MessageForm))
        self.assertFalse(form.is_bound)
        blocked_dm = response.context['blocked_dm']
        self.assertTrue(blocked_dm)
    
    def test_get_report(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversation.html')
        form = response.context['report_form']
        self.assertTrue(isinstance(form, ReportForm))
        self.assertFalse(form.is_bound)

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

    def test_get_sets_message_params_to_zero_with_no_messages(self):
        self.conversation.messages.set(Message.objects.none())
        response = self.client.get(self.url)
        first_message = response.context['first_message']
        next_message = response.context['next_message']
        self.assertEqual(first_message,0)
        self.assertEqual(next_message,0)

    def test_first_message_zero_if_specified_but_no_messages_exist(self):
        self.conversation.messages.set(Message.objects.none())
        response = self.client.get(self.url+"?first_message=1")
        first_message = response.context['first_message']
        next_message = response.context['next_message']
        self.assertEqual(first_message,0)
        self.assertEqual(next_message,0)

    def test_first_message_set_to_other_if_specified_but_that_message_does_not_exist(self):
        response = self.client.get(self.url+"?first_message=2")
        first_message = response.context['first_message']
        next_message = response.context['next_message']
        self.assertEqual(first_message,4)
        self.assertEqual(next_message,1)

    def test_first_message_specified_after_sending_message_to_empty_conversation(self):
        self.form_input['first_message'] = '0'
        self.conversation.messages.set(Message.objects.none())
        response = self.client.post(self.url, data=self.form_input,follow=True)
        first_message = response.context['first_message']
        next_message = response.context['next_message']
        self.assertEqual(first_message,6)
        self.assertEqual(next_message,6)

    def test_unsuccessful_message_send(self):
        self.form_input['content'] = ''
        before_count = Message.objects.count()
        response = self.client.post(self.url,data=self.form_input,follow=True)
        after_count = Message.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertRedirects(response, self.url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        form = response.context['message_form']
        self.assertTrue(isinstance(form, MessageForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_direct_message_send_if_user_is_blocked(self):
        self.form_input['content'] = '123'
        blocked_user = User.objects.get(username='@johndoe')
        self.user.blocked_users.add(blocked_user)
        before_count = Message.objects.count()
        response = self.client.post(self.url,data=self.form_input)
        after_count = Message.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 302)

    def test_successful_message_send(self):
        before_count = Message.objects.count()
        response = self.client.post(self.url, data=self.form_input,follow=True)
        after_count = Message.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertRedirects(response, self.url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
        message = self.conversation.messages.last()
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.content, 'Ploof')
        self.assertIn(message,self.conversation.messages.all())
        form = response.context['message_form']
        self.assertTrue(isinstance(form, MessageForm))
        self.assertFalse(form.is_bound)

    def test_successful_report(self):
        message_id_to_report = self.message.id
        report_data = {
            'action': message_id_to_report,
            'reason': 'abuse'
        }
        before_report_message = Message.objects.get(pk=message_id_to_report)
        self.assertIn(self.user, before_report_message.visible_to.all())
        response = self.client.post(self.url, data=report_data)
        form = ReportForm(data=report_data)
        report_message = Message.objects.get(pk=message_id_to_report)
        self.assertNotIn(self.user, report_message.visible_to.all())
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Report.objects.filter(object_id=report_message.id).exists())
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertIn("Message reported successfully.", str(messages_list[0]))

    def test_unsuccessful_report (self):
        valid_message_id = self.message.id 
        report_data = {
            'action': valid_message_id,
            'reason': 'dfdsdf'
        }
        response = self.client.post(self.url, data=report_data, follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertIn("There was an issue with the report.", str(messages_list[0]))

    def test_successful_delete_message_for_self(self):
        delete_data = {
            'action': self.message.id,
            'delete': 'me'
        }
        visible_to_before = self.message.visible_to.count()
        messages_before = Message.objects.count()
        response = self.client.post(self.url,data=delete_data,follow=True)
        visible_to_after = self.message.visible_to.count()
        messages_after = Message.objects.count()
        self.assertEqual(visible_to_after,visible_to_before-1)
        self.assertEqual(messages_after,messages_before)
        redirect_url = reverse('conversation',kwargs={'conversation_id':self.conversation.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')

    def test_successful_delete_message_for_all_individually(self):
        delete_data = {
            'action': self.message.id,
            'delete': 'me'
        }
        visible_to_before = self.message.visible_to.count()
        messages_before = Message.objects.count()
        response = self.client.post(self.url,data=delete_data,follow=True)
        self.client.logout()
        other_user = User.objects.get(username='@johndoe')
        self.client.login(username=other_user.username, password="Password123")
        response = self.client.post(self.url,data=delete_data,follow=True)
        visible_to_after = self.message.visible_to.count()
        messages_after = Message.objects.count()
        self.assertEqual(visible_to_after,visible_to_before-2)
        self.assertEqual(messages_after,messages_before-1)
        redirect_url = reverse('conversation',kwargs={'conversation_id':self.conversation.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')

    def test_successful_delete_message_for_all_at_once(self):
        delete_data = {
            'action': self.message.id,
            'delete': 'all'
        }
        visible_to_before = self.message.visible_to.count()
        messages_before = Message.objects.count()
        response = self.client.post(self.url,data=delete_data,follow=True)
        visible_to_after = self.message.visible_to.count()
        messages_after = Message.objects.count()
        self.assertEqual(visible_to_after,visible_to_before-2)
        self.assertEqual(messages_after,messages_before-1)
        redirect_url = reverse('conversation',kwargs={'conversation_id':self.conversation.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'conversation.html')
