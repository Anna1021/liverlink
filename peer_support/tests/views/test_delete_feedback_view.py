"""Tests for the delete feedback view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User, Feedback

class DeleteFeedbackViewTestCase(TestCase):
    """Tests for the delete feedback view."""
    
    fixtures = ['peer_support/tests/fixtures/default_admin.json',
                'peer_support/tests/fixtures/default_feedback.json']

    def setUp(self):
        self.feedback = Feedback.objects.get(id=1)
        self.url = reverse('delete_feedback', args=[self.feedback.id])
        self.admin = User.objects.get(username='@admin')
        self.client.force_login(self.admin)

    def test_delete_feedback_url(self):
        self.assertEqual(self.url, '/delete_feedback/1/')

    def test_delete_feedback(self):
        before_count = Feedback.objects.count()
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count = Feedback.objects.count()
        self.assertEqual(before_count - 1, after_count)

    def test_delete_feedback_without_being_logged_in(self):
        before_count = Feedback.objects.count()
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        after_count = Feedback.objects.count()
        self.assertEqual(before_count, after_count)