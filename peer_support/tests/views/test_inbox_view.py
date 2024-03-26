"""Tests for inbox view"""
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User, Notification

class InboxViewTestCase(TestCase):
    """Tests for inbox view."""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/default_friend_request.json',
                'peer_support/tests/fixtures/default_notification.json',
                'peer_support/tests/fixtures/other_notifications.json',]

    def setUp(self):
        self.url = reverse('inbox')
        self.user = User.objects.get(username='@johndoe')
        self.client.force_login(self.user)

    def test_inbox_url(self):
        self.assertEqual(self.url, '/inbox/')

    def test_inbox(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        notifications = response.context['notifications']
        self.assertEqual(notifications.count(), Notification.objects.filter(user=self.user).count())
        self.assertTemplateUsed(response, 'inbox.html')

    def test_inbox_without_being_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertEqual(Notification.objects.count(), 6)