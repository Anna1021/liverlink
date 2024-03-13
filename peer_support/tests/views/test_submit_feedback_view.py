"""Tests for the submit feedback view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.forms import FeedbackForm
from peer_support.models import User, Feedback
from peer_support.tests.helpers import reverse_with_next

class SubmitFeedbackViewTestCase(TestCase):
    """Test suite for the submit feedback view."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('feedback')
        self.form_input = {
            'title': 'Test feedback',
            'content': 'This is test feedback.'
        }

    def test_feedback_url(self):
        self.assertEqual(self.url, '/settings/feedback/')

    def test_get_feedback_form(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'submit_feedback.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, FeedbackForm))

    def test_feedback_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_feedback_submission(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = Feedback.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        after_count = Feedback.objects.count()
        self.assertEqual(before_count + 1, after_count)
        feedback = Feedback.objects.first()
        self.assertEqual(feedback.title, 'Test feedback')
        self.assertEqual(feedback.content, 'This is test feedback.')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "Feedback has been successfully submitted.")

    def test_unsuccessful_feedback_submission_with_invalid_input(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = Feedback.objects.count()
        self.form_input['content'] = '*' * 501
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count = Feedback.objects.count()
        self.assertEqual(before_count, after_count)
