from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from peer_support.models import Report, User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib import messages

class ProfileViewTest(TestCase):
    """Tests of the profile view"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/other_user_profiles.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.user_to_report = User.objects.get(username='@janedoe')
        user_content_type = ContentType.objects.get_for_model(self.user_to_report)
        self.report_user = Report.objects.create(
            reporter=self.user,  
            reason='spam',  
            reported_at=timezone.now(),
            content_type=user_content_type,
            object_id=self.user_to_report.pk,
            content_object=self.user_to_report,
        )
        self.url = reverse('profile', kwargs={'username':self.user_to_report})
        self.client.force_login(self.user)
    
    def test_successful_report_profile(self):
        report_data = {
            'action': self.user_to_report.pk,
            'reason': 'abuse'
        }
        response = self.client.post(self.url, data=report_data)
        self.assertEqual(response.status_code, 302) 
        content_type = ContentType.objects.get_for_model(User)
        report_exists = Report.objects.filter(
            content_type=content_type,
            object_id=self.user_to_report.pk,
            reason='abuse',
            reporter=self.user
        ).exists()
        self.assertTrue(report_exists, "The report should exist in the database.")

    def test_unsuccessful_report_profile(self):
        valid_message_id = 1  
        report_data = {
            'action': valid_message_id,
            'reason': 'dfdsdf'
        }
        response = self.client.post(self.url, data=report_data, follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertIn("There was an issue with the report.", str(messages_list[0]))
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
        self.assertRedirects(response, redi