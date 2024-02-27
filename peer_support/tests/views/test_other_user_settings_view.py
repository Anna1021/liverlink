"""Tests of the other users profile settings view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User

class OtherUserSettingsViewTestCase(TestCase):
    """Tests of the other users profile settings view."""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('other_user_settings')
        self.client.login(username=self.user.username, password='Password123')

    def test_other_user_settings_url(self):
        self.assertEqual(self.url, '/settings/other_users/')

    def test_other_user_settings(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'other_user_settings.html')
        self.assertQuerySetEqual(response.context['block_list'], self.user.blocked_users.all())

    def test_block_list_contains_all_blocked_users(self):
        for user_id in range(2,8):
            self.user.blocked_users.add(User.objects.get(id=user_id))
        blocked_users_count = self.user.blocked_users.count()
        self.assertEqual(blocked_users_count, 6)
        response = self.client.get(self.url)
        self.assertQuerySetEqual(response.context['block_list'], self.user.blocked_users.all())
        self.assertEqual(len(response.context['block_list']), blocked_users_count)
        for user in response.context['block_list']:
            self.assertIn(user, self.user.blocked_users.all())

    def test_other_user_settings_without_being_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
