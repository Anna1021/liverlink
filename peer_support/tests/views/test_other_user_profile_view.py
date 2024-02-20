"""Tests of the other user profile view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User

class OtherUserProfileViewTestCase(TestCase):
    """Tests of the other user profile view."""

    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('other_user_profile',kwargs={'username':self.user.username})
        self.client.login(username=self.user.username, password="Password123")

    def test_other_user_profile_url(self):
        self.assertEqual(self.url,'/other_user_profile/@johndoe/')

    def test_get_other_user_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'other_user_profile.html')
        user = response.context['user']
        self.assertEqual(user, self.user)

    def test_get_other_user_profile_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)