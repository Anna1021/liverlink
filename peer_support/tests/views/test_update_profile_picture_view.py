"""Tests for the update profile picture view."""
import json
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User

class UpdateProfilePictureViewTestCase(TestCase):
    """Tests for the update profile picture view."""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/default_user_profile.json']

    def setUp(self):
        self.url = reverse('update_profile_picture')
        self.user = User.objects.get(username='@johndoe')
        self.client.force_login(self.user)

    def test_update_profile_picture_url(self):
        self.assertEqual(self.url, '/update_profile_picture/')

    def test_update_profile_picture(self):
        data = {'profile_picture': 'profile_pictures/Firefly Create a social media avatar of a asian teenage boy in casual clothing 80817.jpg'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(self.user.userprofile.profile_picture, 'profile_pictures/Firefly Create a social media avatar of a asian teenage boy in casual clothing 80817.jpg')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

    def test_update_profile_picture_without_profile_picture(self):
        data = {'profile_picture': ''}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'fail'})

    def test_update_profile_picture_without_being_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)