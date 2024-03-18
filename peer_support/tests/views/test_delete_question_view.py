from django.test import TestCase, Client
from peer_support.models import Question, Response, User
from django.urls import reverse
from django.contrib.messages import get_messages

class DeleteQuestionTestCase(TestCase):
    """Tests for the Delete Question view."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='@janedoe')
        self.client.login(username=self.user.username, password="Password123")
        self.question = Question.objects.create(title='Test Question', body='This is a test question.', author=self.user)
        self.response = Response.objects.create(body='Test Response', user=self.user, question=self.question)
        self.login_url = reverse('log_in')  # Define this here for consistency across tests.
        self.url = reverse('delete_question', kwargs={'id':self.question.id})
        self.redirect_url = reverse('resources')

    def test_question_url(self):
        self.assertEqual(self.url,'/delete_question/1/')

    def test_successful_delete_question_for_self(self):
        questions_before = Question.objects.count()
        response = self.client.get(self.url, follow=True)
        questions_after = Question.objects.count()
        self.assertEqual(questions_after, questions_before -1)
        redirect_url = reverse('resources')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'resources.html')

    def test_unsuccessful_delete_nonexistent_question(self):
        non_existent_question_id = 999999
        delete_url = reverse('delete_question', kwargs={'id': non_existent_question_id})
        response = self.client.get(delete_url, follow=True)
        expected_redirect_url = reverse('resources')
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)
        messages = [str(message) for message in get_messages(response.wsgi_request)]
        self.assertIn('The question does not exist.', messages)
