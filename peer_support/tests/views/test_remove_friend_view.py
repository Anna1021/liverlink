"""Tests of the remove friend view."""
from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User

class RemoveFriendViewTestCase(TestCase):
    """Tests of the remove friend view."""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.friend_user = User.objects.get(username='@janedoe')
        self.url = reverse('remove_friend', args=[self.friend_user.id])
        self.client.login(username=self.user.username, password='Password123')

    def test_remove_friend_url(self):
        self.assertEqual(self.url, '/remove_friend/2')

    def test_remove_friend(self):
        self.assertEqual(self.user.friends.all().count(), 0)
        self.user.friends.add(self.friend_user)
        self.assertEqual(self.user.friends.all().count(), 1)
        self.assertEqual(self.friend_user.friends.all().count(), 1)
        self.assertIn(self.friend_user, self.user.friends.all())
        self.assertIn(self.user, self.friend_user.friends.all())
        before_count = self.user.friends.all().count()
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        after_count = self.user.friends.all().count()
        self.assertEqual(before_count - 1, after_count)
        self.assertNotIn(self.friend_user, self.user.friends.all())
        self.assertNotIn(self.user, self.friend_user.friends.all())

    def test_remove_friend_if_user_is_not_friend_has_no_effect(self):
        self.assertEqual(self.user.friends.all().count(), 0)
        self.assertNotIn(self.friend_user, self.user.friends.all())
        self.assertNotIn(self.user, self.friend_user.friends.all())
        before_count = self.user.friends.all().count()
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        after_count = self.user.friends.all().count()
        self.assertEqual(before_count, after_count)
        self.assertNotIn(self.friend_user, self.user.friends.all())
        self.assertNotIn(self.user, self.friend_user.friends.all())

    def test_remove_friend_without_being_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
