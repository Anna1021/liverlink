"""Tests of the other user profile view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User

class OtherUserProfileViewTestCase(TestCase):
    """Tests of the other user profile view."""

    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/default_parent.json',
                'peer_support/tests/fixtures/other_patients.json',
                'peer_support/tests/fixtures/other_mentors.json',
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

    def test_get_other_user_profile_parent(self):
        url = reverse('other_user_profile', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'other_user_profile.html')
        parent = response.context['parent']
        self.assertEqual(parent, self.user.parent)

    def test_get_other_user_profile_patient(self):
        user = User.objects.get(username='@janedoe')
        url = reverse('other_user_profile', kwargs={'username': user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'other_user_profile.html')
        patient = response.context['patient']
        self.assertEqual(patient, user.patient)

    def test_get_other_user_profile_mentor(self):
        user = User.objects.get(username='@alexsmith')
        url = reverse('other_user_profile', kwargs={'username': user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'other_user_profile.html')
        mentor = response.context['mentor']
        self.assertEqual(mentor, user.mentor)

    def test_get_other_user_profile_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)