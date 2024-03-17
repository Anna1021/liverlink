"""Tests of the unblock user view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User

class UnblockUserViewTestCase(TestCase):
    """Tests of the unblock user view."""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.second_user = User.objects.get(username='@janedoe')
        self.user.blocked_users.add(self.second_user)
        self.url = reverse('unblock_user', args=[self.second_user.id])
        self.client.force_login(self.user)

    def test_unblock_user_url(self):
        self.assertEqual(self.url, '/unblock_user/2')

    def test_unblock_user(self):
        before_count = self.user.blocked_users.count()
        self.assertIn(self.second_user, self.user.blocked_users.all())
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count = self.user.blocked_users.count()
        self.assertEqual(before_count - 1, after_count)
        self.assertNotIn(self.second_user, self.user.blocked_users.all())

    def test_unblock_user_without_being_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
