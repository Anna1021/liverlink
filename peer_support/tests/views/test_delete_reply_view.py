from django.test import TestCase, Client
from peer_support.models import Question, Response, User
from django.urls import reverse
from django.contrib.messages import get_messages

class DeleteReplyTestCase(TestCase):
    """Tests for the Delete Reply view."""

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
        self.url = reverse('delete_reply', kwargs={'reply_id':self.response.id})
        self.redirect_url = reverse('question', kwargs={'id': self.question.id})

    def test_question_url(self):
        self.assertEqual(self.url,'/delete_reply/1/')

    def test_successful_delete_reply_for_self(self):
        replies_before = Response.objects.count()
        response = self.client.post(self.url, follow=True)
        replies_after = Response.objects.count()
        self.assertEqual(replies_after, replies_before - 1)
        redirect_url = reverse('question', kwargs={'id': self.question.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'question.html') 

    def test_unsuccessful_delete_nonexistent_reply(self):
        non_existent_reply_id = 999999
        delete_url = reverse('delete_reply', kwargs={'reply_id': non_existent_reply_id})
        response = self.client.post(delete_url, follow=True) 
        expected_redirect_url = reverse('resources')
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)
        messages = [str(message) for message in get_messages(response.wsgi_request)]
        self.assertIn('The reply does not exist.', messages)
        self.assertTemplateUsed(response, 'resources.html') 

