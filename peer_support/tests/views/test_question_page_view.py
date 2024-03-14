"""Tests of the Question Page view."""
from django.test import TestCase, Client
from peer_support.models import Question, Response, User
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

    def test_question_page_GET(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'question.html')
        self.assertIsInstance(response.context['response_form'], NewResponseForm)

    def test_question_page_invalid_POST(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('response_form' in response.context and response.context['response_form'].errors)

    def test_question_page_valid_POST(self):
        self.client.login(username=self.user.username, password='Password123')
        form_data = {'body': 'This is a test response.'}
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Response.objects.filter(body='This is a test response.', user=self.user, question=self.question).exists())
        response_id = Response.objects.get(body='This is a test response.', user=self.user, question=self.question).id
        self.assertRedirects(response, f'/question/{self.question.id}#{response_id}')
