"""Tests for the information view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.models import User
from peer_support.tests.helpers import reverse_with_next

class InformationViewTestCase(TestCase):
    """Test suite for the accessibility view."""

    fixtures = ['peer_support/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('accessibility')

    def test_information_url(self):
        self.assertEqual(self.url, '/accessibility/')

    def test_information_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_request_returns_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accessibility.html')
    