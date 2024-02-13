from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from peer_support.models import Question, Response

User = get_user_model()
class ReplyPageTest(TestCase):
    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.url = reverse('resources')
        self.user = User.objects.get(username='@johndoe')
        self.question = Question.objects.create(title='Test Question', body='Test Body', author=self.user)
        self.response = Response.objects.create(body='Test Response', user=self.user, question=self.question)

    def test_access_page_logged_in(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resources.html')

    def test_post_valid_reply(self):
        self.client.login(username=self.user.username, password='Password123')
        form_data = {
            'body': 'This is a valid reply.',
            'question': self.question.id,
            'parent': self.response.id
        }
        response = self.client.post(self.url, form_data)
        new_reply = Response.objects.latest('id')
        expected_url = f'/question/{self.question.id}#{new_reply.id}'
        self.assertEqual(response.status_code, 200)


    def test_post_invalid_reply(self):
        self.client.login(username=self.user.username, password='Password123')
        form_data = {
            'body': '',
            'question': self.question.id,
            'parent': self.response.id
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertFalse(form.is_valid())

    def test_post_invalid_reply(self):
        self.client.login(username=self.user.username, password='Password123')
        form_data = {
            'body': '',
            'question': self.question.id,
            'parent': self.response.id
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
