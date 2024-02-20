"""Tests of the friends list view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User, FriendRequest, Notification

class FriendsListView(TestCase):
    """Tests of the friends list view."""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',]
    
    def setUp(self):
        self.url = reverse('friends_list')
        self.user = User.objects.get(username='@petrapickles')
        self.client.force_login(self.user)

    def test_friends_list_url(self):
        self.assertEqual(self.url, '/friends_list/')
        
    def test_friends_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'friends_list.html')
        self.assertEqual(len(response.context['friends']), 1)
        self.assertEqual(response.context['friends'][0], User.objects.get(username='@peterpickles'))

    def test_friends_list_without_being_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)