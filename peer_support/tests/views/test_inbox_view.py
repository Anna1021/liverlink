"""Tests for inbox view"""
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import *
from django.utils import timezone
from datetime import timedelta

from django.contrib.contenttypes.models import ContentType
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
        notification = Notification.objects.get(pk=3)
        content_type = ContentType.objects.get(model='groupconversation')
        notification.content_type = content_type
        notification.save()
        notification = Notification.objects.get(pk=5)
        content_type = ContentType.objects.get(model='post')
        notification.content_type = content_type
        notification.save()
        notification = Notification.objects.get(pk=6)
        content_type = ContentType.objects.get(model='question')
        notification.content_type = content_type
        notification.save()

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

    def test_filter_notifications_by_type_and_timeframe(self):
        notification_comemnt_5 = Notification.objects.get(pk=5)
        notification_response_6 = Notification.objects.get(pk=6)
        notification_response_6.created = timezone.now() - timedelta(days=5)
        notification_response_6.save()
        response = self.client.get(self.url, {'timeframe': 'past_7_days'})
        self.assertEqual(response.status_code, 200)
        filtered_notifications = response.context['notifications']
        self.assertIn(notification_response_6, filtered_notifications)
        self.assertNotIn(notification_comemnt_5, filtered_notifications)
        self.assertEqual(len(filtered_notifications), 1)
        self.assertTrue(all(notification.title == 'New Response' for notification in filtered_notifications))
        self.assertTrue(all(notification.created >= timezone.now() - timedelta(days=7) for notification in filtered_notifications))

    def test_no_filtering(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        notifications = Notification.objects.all()
        filtered_notifications = response.context['notifications']
        self.assertEqual(len(filtered_notifications), len(notifications))
        for notification in notifications:
            self.assertIn(notification, filtered_notifications)

    def test_filter_notifications_by_type_only(self):
        response = self.client.get(self.url, {'type': 'friend request'})
        self.assertEqual(response.status_code, 200)
        filtered_notifications = response.context['notifications']
        self.assertEqual(len(filtered_notifications), 1)
        self.assertTrue(all(notification.title == 'New Friend Request' for notification in filtered_notifications))
    
    def test_filter_notifications_by_timeframe_only(self):
        notification = Notification.objects.get(pk=4)
        notification.created = timezone.now() - timedelta(hours=12)
        notification.save()
        response = self.client.get(self.url, {'timeframe': 'past_24_hours'})
        self.assertEqual(response.status_code, 200)
        request = response.wsgi_request
        filtered_notifications = response.context['notifications']
        self.assertEqual(len(filtered_notifications), 1)
        self.assertTrue(all(notification.created >= timezone.now() - timedelta(hours=24) for notification in filtered_notifications))