"""Tests of the other user profile view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User

class ProfileViewTestCase(TestCase):
    """Tests of the other user profile view."""

    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/default_parent.json',
                'peer_support/tests/fixtures/other_patients.json',
                'peer_support/tests/fixtures/other_mentors.json',
            ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('profile',kwargs={'username':self.user.username})
        self.client.login(username=self.user.username, password="Password123")

    def test_profile_url(self):
        self.assertEqual(self.url,'/profile/@johndoe/')

    def test_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        user = response.context['user']
        self.assertEqual(user, self.user)

    def test_get_profile_parent(self):
        url = reverse('profile', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        parent = response.context['parent']
        self.assertEqual(parent, self.user.parent)

    def test_get_profile_patient(self):
        user = User.objects.get(username='@janedoe')
        url = reverse('profile', kwargs={'username': user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        patient = response.context['patient']
        self.assertEqual(patient, user.patient)

    def test_get_profile_mentor(self):
        user = User.objects.get(username='@alexsmith')
        url = reverse('profile', kwargs={'username': user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        mentor = response.context['mentor']
        self.assertEqual(mentor, user.mentor)

    def test_get_profile_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)