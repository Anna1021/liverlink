"""Tests for the delete notification view."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User, Notification, FriendRequest

class DeleteNotificationViewTestCase(TestCase):
    """Tests for the delete notification view."""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/default_friend_request.json',
                'peer_support/tests/fixtures/default_notification.json',
                'peer_support/tests/fixtures/other_notifications.json',]

    def setUp(self):
        self.url = reverse('delete_notification', args=[1])
        self.user = User.objects.get(username='@johndoe')
        self.client.force_login(self.user)

    def test_delete_notification_url(self):
        self.assertEqual(self.url, '/delete_notification/1/')

    def test_delete_notification(self):
        self.assertEqual(Notification.objects.count(), 3)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Notification.objects.count(), 2)

    def test_delete_notification_with_friend_request(self):
        friend_request = FriendRequest.objects.get(id=1)
        friend_request_notification = Notification.objects.get(id=2)
        friend_request_notification.content_type = ContentType.objects.get_for_model(FriendRequest)
        friend_request_notification.content_object = friend_request
        friend_request_notification.save()
        self.assertTrue(friend_request_notification.get_is_friend_request())
        before_friend_request_count = FriendRequest.objects.count()
        self.assertEqual(Notification.objects.count(), 3)
        response = self.client.get(reverse('delete_notification', args=[2]), follow=True)
        after_friend_request_count = FriendRequest.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Notification.objects.count(), 2)
        self.assertEqual(before_friend_request_count - 1, after_friend_request_count)

    def test_delete_notification_without_being_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertEqual(Notification.objects.count(), 3)