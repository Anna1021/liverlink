"""Tests of the home view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.models import User

class HomeViewTestCase(TestCase):
    """Tests of the home view."""

    fixtures = ['peer_support/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.get(username='@johndoe')

    def test_home_url(self):
        self.assertEqual(self.url,'/')

    def test_get_home(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_get_home_redirects_when_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
   
    def test_first_login(self):
        self.assertTrue(self.user.first_login)

    def test_second_login(self):
        self.user.first_login = False
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')