"""Tests of the accept friend request view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User, FriendRequest, Notification

class AcceptFriendRequestViewTestCase(TestCase):
    """Tests of the accept friend request view."""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/default_friend_request.json',
                'peer_support/tests/fixtures/other_friend_requests.json',
                ]

    def setUp(self):
        self.url = reverse('accept_friend_request', args=[1, 2])
        self.user = User.objects.get(username='@janedoe')
        self.friend_user = User.objects.get(username='@johndoe')
        self.client.force_login(self.user)

    def test_accept_friend_request_url(self):
        self.assertEqual(self.url, '/accept_friend_request/1/2/')

    def test_accept_friend_request(self):
        friend_request = FriendRequest.objects.get(id=1)
        self.assertNotIn(self.user, self.friend_user.friends.all())
        self.assertFalse(friend_request.is_accepted)
        self.assertEqual(Notification.objects.count(), 0)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.user, self.friend_user.friends.all())
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.last()
        self.assertEqual(notification.title, 'Friend Request Accepted')
        self.assertEqual(notification.description, '@janedoe accepted your friend request.')
        self.assertEqual(notification.user, User.objects.get(username='@johndoe'))
        self.assertEqual(self.user.friends.count(), 1)
        self.assertEqual(self.user.friends.first().username, '@johndoe')

    def test_accept_friend_request_without_being_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)