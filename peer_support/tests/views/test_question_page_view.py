"""Tests of the Question Page view."""
from django.test import TestCase, Client
from django.contrib.contenttypes.models import ContentType
from peer_support.models import Question, Response, User, Notification
from peer_support.forms import NewResponseForm
from django.urls import reverse

class QuestionPageTestCase(TestCase):
    """Tests of the Question Page view."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.question = Question.objects.create(title='Test Question', body='This is a test question.', author=self.user)
        self.response = Response.objects.create(body='Test Response', user=self.user, question=self.question)
        self.client = Client()
        self.url = reverse('question', args=(self.question.id,))
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


