from django.test import TestCase
from django.urls import reverse
from peer_support.models import User

class NewQuestionPageTest(TestCase):
    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.url = reverse('new-question')
        self.user = User.objects.get(username='@johndoe')
    def test_access_page_logged_in(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new-question.html')

    def test_access_page_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('log_in') + "?next=" + self.url)

    def test_post_valid_data(self):
        self.client.login(username=self.user.username, password='Password123')
        form_data = {
            'title': 'Test Question',
            'body': 'Test body content.'
        }
        response = self.client.post(self.url, form_data)
        self.assertRedirects(response, reverse('resources'))

    def test_post_invalid_title(self):
        self.client.login(username=self.user.username, password='Password123')
        form_data = {
            'title': '',
            'body': 'Test body content.'
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue('title' in response.context['form'].errors)

    def test_post_invalid_body(self):
        self.client.login(username=self.user.username, password='Password123')
        form_data = {
            'title': 'Test Question',
            'body': ''
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue('body' in response.context['form'].errors)


