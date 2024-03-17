"""Tests for the customisation view."""
import os
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from django.contrib.staticfiles import finders
from peer_support.models import User
from peer_support.views.customisation_view import CustomisationView

class CustomisationViewTestCase(TestCase):
    """Tests for the customisation view."""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',]

    def setUp(self):
        self.url = reverse('customisation')
        self.user = User.objects.get(username='@johndoe')
        self.client.force_login(self.user)

    def test_customisation_url(self):
        self.assertEqual(self.url, '/customisation/')

    def test_customisation(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        profile_pictures = response.context['profile_pictures']
        self.assertIsInstance(profile_pictures, list)
        self.assertTemplateUsed(response, 'customisation.html')

    def test_get_profile_pictures(self):
        view = CustomisationView()
        profile_pictures = view.get_profile_pictures()
        self.assertIsInstance(profile_pictures, list)
        expected_profile_pictures = os.listdir(finders.find('profile_pictures'))
        self.assertEqual(set(profile_pictures), set(expected_profile_pictures))

    def test_customisation_without_being_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)