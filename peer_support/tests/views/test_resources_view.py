"""Tests of the Resources view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.models import User,Question
from peer_support.tests.helpers import reverse_with_next

class ResourcesViewTestCase(TestCase):
    """Tests of the Resources view."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_questions.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.force_login(self.user)
        self.url = reverse('resources')

    def test_resources_redirects_when_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/resources/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resources.html')

    def test_pagination_is_correct(self):
        for i in range(6):
            Question.objects.create(
                author=self.user,
                title="Test for pagination",
                body="Page should only have 10 questions"
            )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('questions' in response.context)
        self.assertEqual(len(response.context['questions']), 10)

    def test_questions_ordered_by_created_at(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        questions = response.context['questions']
        self.assertTrue(all(questions[i].created_at >= questions[i + 1].created_at for i in range(len(questions) - 1)))
