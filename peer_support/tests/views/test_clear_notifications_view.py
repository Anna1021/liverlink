"""Tests for the clear notifications view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User, Notification

class ClearNotificationsViewTestCase(TestCase):
    """Tests for the clear notifications view."""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/default_friend_request.json',
                'peer_support/tests/fixtures/default_notification.json',
                'peer_support/tests/fixtures/other_notifications.json',]

    def setUp(self):
        self.url = reverse('clear_notifications')
        self.user = User.objects.get(username='@johndoe')
        self.client.force_login(self.user)

    def test_clear_notifications_url(self):
        self.assertEqual(self.url, '/clear_notifications/')

    def test_clear_notifications(self):
        self.assertEqual(Notification.objects.count(), 3)
        user_notifications = Notification.objects.filter(user=self.user)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Notification.objects.count(), Notification.objects.exclude(user=self.user).count())
        self.assertEqual(user_notifications.count(), 0)

    def test_clear_notifications_without_being_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertEqual(Notification.objects.count(), 3)