"""Tests of the feedback view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.models import User
from django.contrib.messages import get_messages
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User, Feedback

class FeedbackViewTestCase(TestCase):
    """Tests of the feedback view."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/default_feedback.json',
        'peer_support/tests/fixtures/other_feedback.json'
    ]

    def setUp(self):
        self.url = reverse('feedback')
        self.admin_user = User.objects.get(username='@admin')
        self.client.force_login(self.admin_user)

    def test_get_feedback_redirects_when_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_non_staff_cannot_view_feedback(self):
        self.client.logout()
        self.client.force_login(User.objects.get(username='@johndoe'))
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('dashboard'))  
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have access to this view.")

    def test_staff_can_view_feedback(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback.html')

    def test_feedback_is_in_reverse_chronological_order(self):
        response = self.client.get(self.url)
        feedback_count = Feedback.objects.count()
        self.assertTrue('feedback' in response.context)
        self.assertEqual(len(response.context['feedback']), feedback_count)
        ordered_feedback = Feedback.objects.order_by('-submitted_at')
        self.assertQuerySetEqual(response.context['feedback'], ordered_feedback)
