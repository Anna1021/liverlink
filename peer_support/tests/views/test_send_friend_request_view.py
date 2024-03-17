"""Tests of the send friend request view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User, FriendRequest, Notification

class SendFriendRequestViewTestCase(TestCase):
    """Tests of the send friend request view."""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',]

    def setUp(self):
        self.url = reverse('send_friend_request', args=[2])
        self.user = User.objects.get(username='@johndoe')
        self.client.force_login(self.user)

    def test_send_friend_request_url(self):
        self.assertEqual(self.url, '/send_friend_request/2')

    def test_send_friend_request(self):
        self.assertEqual(FriendRequest.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FriendRequest.objects.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)
        friend_request = FriendRequest.objects.first()
        self.assertEqual(friend_request.sender, self.user)
        self.assertEqual(friend_request.receiver, User.objects.get(username='@janedoe'))
        notification = Notification.objects.first()
        self.assertEqual(notification.title, 'Friend Request')
        self.assertEqual(notification.description, '@johndoe sent you a friend request.')
        self.assertEqual(notification.user, User.objects.get(username='@janedoe'))
        self.assertEqual(notification.friend_request, friend_request)

    def test_send_friend_request_without_being_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
