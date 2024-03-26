"""Tests of the Question Page view."""
from django.test import TestCase, Client
from django.contrib.contenttypes.models import ContentType
from peer_support.models import Question, Response, User, Report, Notification
from peer_support.forms import NewResponseForm
from django.urls import reverse
from django.contrib import messages

class QuestionPageTestCase(TestCase):
    """Tests of the Question Page view."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_question.json',
        'peer_support/tests/fixtures/default_response.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.question = Question.objects.first()
        self.response = Response.objects.first()
        self.client = Client()
        self.url = reverse('question', args=(self.question.id,))
        self.client.force_login(self.user)
        self.reply_url = reverse('question', args=(self.question.id,))
        self.user = User.objects.get(username='@johndoe')
        self.second_question = Question.objects.create(title='Test Question', body='Test Body', author=self.user)
        self.second_response = Response.objects.create(body='Test Response', user=self.user, question=self.question)
        self.response_id = Response.objects.get(body='Test Response', user=self.user, question=self.question).id
        self.reply_form_data = {
            'body': 'Test Reply Body',
            'question': self.question.id,
            'parent': self.response_id  
        }
        self.client.force_login(self.user)

    def test_question_page_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'question.html')
        self.assertIsInstance(response.context['response_form'], NewResponseForm)

    def test_question_page_invalid_POST(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('response_form' in response.context and response.context['response_form'].errors)

    def test_question_page_valid_POST(self):
        form_data = {'body': 'This is a test response.'}
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Response.objects.filter(body='This is a test response.', user=self.user, question=self.question).exists())
        response_id = Response.objects.get(body='This is a test response.', user=self.user, question=self.question).id
        self.assertRedirects(response, f'/question/{self.question.id}#{response_id}')

    def test_question_page_valid_POST_sends_notification(self):
        form_data = {'body': 'This is a test response.'}
        replying_user = User.objects.get(id=2)
        self.client.logout()
        self.client.force_login(replying_user)
        notification_before_count = Notification.objects.count()
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        notification_after_count = Notification.objects.count()
        self.assertEqual(notification_before_count + 1, notification_after_count)
        self.assertTrue(Response.objects.filter(body='This is a test response.', user=replying_user, question=self.question).exists())
        response = Response.objects.get(body='This is a test response.', user=replying_user, question=self.question)
        content_type_id = ContentType.objects.get_for_model(Response)
        notification = Notification.objects.get(content_type=content_type_id, object_id=response.id)
        self.assertEqual(notification.title, "New Response")
        self.assertEqual(notification.description, "@janedoe has replied to your question.")
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.notifying_user, replying_user)
        self.assertEqual(notification.content_type, content_type_id)
        self.assertEqual(notification.object_id, response.id)
        self.assertEqual(notification.content_object, response)

    def test_question_page_valid_POST_does_not_send_notification_if_question_has_same_author(self):
        form_data = {'body': 'This is a test response.'}
        notification_before_count = Notification.objects.count()
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        notification_after_count = Notification.objects.count()
        self.assertEqual(notification_before_count, notification_after_count)
        response = Response.objects.last()
        content_type_id = ContentType.objects.get_for_model(Response)
        self.assertFalse(Notification.objects.filter(content_type=content_type_id, object_id=response.id).exists())

    def test_report_question_valid(self):
        initial_report_count = Report.objects.all().count()
        form_data = {
            'report_question': True,
            'action': self.question.id,
            'reason': 'abuse'
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), "Comment reported successfully.")
        final_report_count = Report.objects.all().count()
        self.assertEqual(final_report_count, initial_report_count + 1, "Report count did not increase as expected.")

    def test_report_response_valid(self):
        initial_report_count = Report.objects.all().count()
        form_data = {
            'report_response': True,
            'action': self.response.id,
            'reason': 'abuse'
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), "Response reported successfully.")
        final_report_count = Report.objects.all().count()
        self.assertEqual(final_report_count, initial_report_count + 1, "Report count did not increase as expected.")

    def test_report_question_invalid(self):
        initial_report_count = Report.objects.all().count()
        form_data = {
            'report_question': True,
            'action': self.question.id,
            'reason': 'dgfdd'
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302, "The response unexpectedly resulted in a redirect.")
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertNotEqual(str(messages_list[0]), "Comment reported successfully.")
        final_report_count = Report.objects.all().count()
        self.assertEqual(final_report_count, initial_report_count, "Report count unexpectedly increased.")

    def test_report_response_invalid(self):
        initial_report_count = Report.objects.filter(object_id=self.response.id, content_type__model='response').count()
        form_data = {
            'report_response': True,
            'action': self.response.id,
            'reason': 'dgfdd' 
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302, "The response unexpectedly resulted in a redirect.")
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertNotEqual(str(messages_list[0]), "Response reported successfully.")
        final_report_count = Report.objects.all().count()
        self.assertEqual(final_report_count, initial_report_count, "Report count unexpectedly increased.")

    def test_access_page_logged_in(self): 
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'question.html')


    def test_get_reply(self):
        response = self.client.get(self.reply_url)
        self.assertEqual(response.status_code, 200)


    def test_valid_reply_creation(self):
        response_count_before = Response.objects.count()
        response = self.client.post(self.reply_url, self.reply_form_data)
        response_count_after = Response.objects.count()
        self.assertEqual(response_count_after, response_count_before + 1)
        new_reply = Response.objects.latest('id')
        self.assertEqual(new_reply.parent, self.response)
        question_detail_url = reverse('question', kwargs={'id': self.question.id})
        expected_redirect_url = f'{question_detail_url}#{new_reply.id}'
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)
        self.assertEqual(new_reply.body, self.reply_form_data['body'])
        self.assertEqual(new_reply.user, self.user)
        self.assertEqual(new_reply.question, self.question)

    def test_valid_reply_creation_sends_notification_to_parent_and_question_authors(self):
        self.client.logout()
        replying_user = User.objects.get(id=2)
        self.client.force_login(replying_user)
        response_count_before = Response.objects.count()
        notification_count_before = Notification.objects.count()
        self.client.post(self.url, self.reply_form_data)
        response_count_after = Response.objects.count()
        notification_count_after = Notification.objects.count()
        self.assertEqual(response_count_after, response_count_before + 1)
        self.assertEqual(notification_count_after, notification_count_before + 2)
        new_reply = Response.objects.latest('id')
        notification_reply = Notification.objects.get(id=1)
        content_type_id = ContentType.objects.get_for_model(Response)
        self.assertEqual(notification_reply.title, "New Response")
        self.assertEqual(notification_reply.description, "@janedoe has replied to your reply.")
        self.assertEqual(notification_reply.user, self.user)
        self.assertEqual(notification_reply.notifying_user, replying_user)
        self.assertEqual(notification_reply.content_type, content_type_id)
        self.assertEqual(notification_reply.object_id, new_reply.id)
        self.assertEqual(notification_reply.content_object, new_reply)
        notification_question = Notification.objects.get(id=2)
        content_type_id = ContentType.objects.get_for_model(Response)
        self.assertEqual(notification_question.title, "New Response")
        self.assertEqual(notification_question.description, "@janedoe has replied to your question.")
        self.assertEqual(notification_question.user, self.user)
        self.assertEqual(notification_question.notifying_user, replying_user)
        self.assertEqual(notification_question.content_type, content_type_id)
        self.assertEqual(notification_question.object_id, new_reply.id)
        self.assertEqual(notification_question.content_object, new_reply)

    def test_valid_reply_creation_does_not_send_notification_if_post_is_same_author(self):
        parent_author = User.objects.get(id=2)
        self.response.user = parent_author
        self.response.save()
        response_count_before = Response.objects.count()
        notification_count_before = Notification.objects.count()
        self.client.post(self.url, self.reply_form_data)
        response_count_after = Response.objects.count()
        notification_count_after = Notification.objects.count()
        self.assertEqual(response_count_after, response_count_before + 1)
        self.assertEqual(notification_count_after, notification_count_before + 1)
        new_reply = Response.objects.latest('id')
        notification_reply = Notification.objects.first()
        content_type_id = ContentType.objects.get_for_model(Response)
        self.assertEqual(notification_reply.title, "New Response")
        self.assertEqual(notification_reply.description, "@johndoe has replied to your reply.")
        self.assertEqual(notification_reply.user, parent_author)
        self.assertEqual(notification_reply.notifying_user, self.user)
        self.assertEqual(notification_reply.content_type, content_type_id)
        self.assertEqual(notification_reply.object_id, new_reply.id)
        self.assertEqual(notification_reply.content_object, new_reply)
        self.assertFalse(Notification.objects.filter(content_type=content_type_id, object_id=new_reply.id, user=self.user).exists())

    def test_valid_reply_creation_does_not_send_notification_if_parent_is_same_author(self):
        post_author = User.objects.get(id=2)
        self.question.author = post_author
        self.question.save()
        response_count_before = Response.objects.count()
        notification_count_before = Notification.objects.count()
        self.client.post(self.reply_url, self.reply_form_data)
        response_count_after = Response.objects.count()
        notification_count_after = Notification.objects.count()
        self.assertEqual(response_count_after, response_count_before + 1)
        self.assertEqual(notification_count_after, notification_count_before + 1)
        new_reply = Response.objects.latest('id')
        notification_reply = Notification.objects.first()
        content_type_id = ContentType.objects.get_for_model(Response)
        self.assertEqual(notification_reply.title, "New Response")
        self.assertEqual(notification_reply.description, "@johndoe has replied to your question.")
        self.assertEqual(notification_reply.user, post_author)
        self.assertEqual(notification_reply.notifying_user, self.user)
        self.assertEqual(notification_reply.content_type, content_type_id)
        self.assertEqual(notification_reply.object_id, new_reply.id)
        self.assertEqual(notification_reply.content_object, new_reply)
        self.assertFalse(Notification.objects.filter(content_type=content_type_id, object_id=new_reply.id, user=self.user).exists())

    def test_valid_reply_creation_does_not_send_notification_if_parent_and_post_are_same_author(self):
        response_count_before = Response.objects.count()
        notification_count_before = Notification.objects.count()
        self.client.post(self.reply_url, self.reply_form_data)
        response_count_after = Response.objects.count()
        notification_count_after = Notification.objects.count()
        self.assertEqual(response_count_after, response_count_before + 1)
        self.assertEqual(notification_count_after, notification_count_before)
        new_reply = Response.objects.latest('id')
        content_type_id = ContentType.objects.get_for_model(Response)
        self.assertFalse(Notification.objects.filter(content_type=content_type_id, object_id=new_reply.id).exists())

    def test_invalid_reply_creation(self):
        response_count_before = Response.objects.count()
        invalid_reply_form_data = {
            'body': '', 
            'question': self.question.id,
            'parent': self.response_id
        }
        response = self.client.post(self.url, invalid_reply_form_data)
        response_count_after = Response.objects.count()
        self.assertEqual(response_count_after, response_count_before)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'question.html')
        self.assertIn('response_form', response.context)
        form = response.context['response_form']
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors)  
        self.assertEqual(form.errors['body'], ['This field is required.'])

    def test_reply_creation_with_parent(self):
        reply_form_data_with_parent = self.reply_form_data.copy()
        reply_form_data_with_parent['parent'] = self.response_id  
        response = self.client.post(self.url, reply_form_data_with_parent)
        new_reply = Response.objects.latest('id')
        self.assertEqual(new_reply.parent.id, self.response_id)
        self.assertTrue(new_reply.parent, "The reply should have a parent.")
        expected_redirect_url = f'/question/{self.question.id}#{new_reply.id}'
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

    def test_reply_creation_without_parent(self):
        reply_form_data_without_parent = self.reply_form_data.copy()
        reply_form_data_without_parent['parent'] = ''  
        response = self.client.post(self.url, reply_form_data_without_parent)
        new_reply = Response.objects.latest('id')
        self.assertIsNone(new_reply.parent)
        expected_redirect_url = f'/question/{self.question.id}#{new_reply.id}'
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)