"""Tests of the other user profile view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User, FriendRequest, Report
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib import messages

class ProfileViewTestCase(TestCase):
    """Tests of the other user profile view."""

    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/default_admin.json',
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

    def test_profile_of_blocked_user(self):
        user_p = User.objects.get(username='@janedoe')
        self.user.blocked_users.add(user_p)
        self.assertIn(user_p, self.user.blocked_users.all())
        url = reverse('profile', kwargs={'username': user_p.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, "You have blocked this user.")
        self.assertContains(response, "Unblock this user")
        self.assertNotContains(response, '<div id="profile-content">')
        self.assertNotContains(response, 'id="friend-link"')
        self.assertNotContains(response, 'id="message-link"')
        user = response.context['user']
        self.assertEqual(user, user_p)
        blocklist = response.context['blocklist']
        self.assertIn(user_p, blocklist)

    def test_profile_of_blocked_by_user(self):
        user_p = User.objects.get(username='@janedoe')
        user_p.blocked_users.add(self.user)
        self.assertIn(self.user, user_p.blocked_users.all())
        url = reverse('profile', kwargs={'username': user_p.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, "You cannot view this user's profile.")
        self.assertNotContains(response, 'id="friend-link"')
        self.assertNotContains(response, 'id="message-link"')
        user = response.context['user']
        self.assertEqual(user, user_p)
        blocklist = response.context['blocklist']
        self.assertIn(self.user, blocklist)

    def test_profile_of_friend_user(self):
        user_p = User.objects.get(username='@janedoe')
        user_p.friends.add(self.user)
        self.assertIn(self.user, user_p.friends.all())
        self.assertIn(user_p, self.user.friends.all())
        url = reverse('profile', kwargs={'username': user_p.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, "Remove friend")
        user = response.context['user']
        self.assertEqual(user, user_p)
        is_friend  = response.context['is_friend']
        self.assertTrue(is_friend)

    def test_profile_of_requested_friend_user(self):
        user_p = User.objects.get(username='@janedoe')
        FriendRequest.objects.create(sender=self.user, receiver=user_p)
        url = reverse('profile', kwargs={'username': user_p.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, "Request sent")
        user = response.context['user']
        self.assertEqual(user, user_p)
        is_friend  = response.context['is_friend']
        self.assertFalse(is_friend)
        request_sent = response.context['request_sent']
        self.assertTrue(request_sent)

    def test_other_user_profile_contains_user_actions_dropdown(self):
        user_p = User.objects.get(username='@janedoe')
        url = reverse('profile', kwargs={'username': user_p.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, 'div id="user-actions-dropdown"')
        user = response.context['user']
        self.assertEqual(user, user_p)

    def test_users_own_profile_contains_settings_button(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, 'div id="profile-settings"')
        user = response.context['user']
        self.assertEqual(user, self.user)

    def test_get_profile_parent(self):
        url = reverse('profile', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
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

    def test_successful_report_profile(self):
        user_to_report = User.objects.get(username='@janedoe')
        user_content_type = ContentType.objects.get_for_model(user_to_report)
        Report.objects.create(reporter=self.user, 
                              reason='spam', 
                              reported_at=timezone.now(), 
                              content_type=user_content_type, 
                              object_id=user_to_report.pk, 
                              content_object=user_to_report
                              )
        url = reverse('profile', kwargs={'username': user_to_report.username})
        report_data = {
            'action': user_to_report.pk,
            'reason': 'abuse'
        }
        response = self.client.post(url, data=report_data)
        self.assertEqual(response.status_code, 302) 
        content_type = ContentType.objects.get_for_model(User)
        report_exists = Report.objects.filter(
            content_type=content_type,
            object_id=user_to_report.pk,
            reason='abuse',
            reporter=self.user
        ).exists()
        self.assertTrue(report_exists, "The report should exist in the database.")

    def test_unsuccessful_report_profile(self):
        user_to_report = User.objects.get(username='@janedoe')
        user_content_type = ContentType.objects.get_for_model(user_to_report)
        Report.objects.create(reporter=self.user, 
                              reason='spam', 
                              reported_at=timezone.now(), 
                              content_type=user_content_type, 
                              object_id=user_to_report.pk, 
                              content_object=user_to_report
                              )
        url = reverse('profile', kwargs={'username': user_to_report.username})
        valid_message_id = 1  
        report_data = {
            'action': valid_message_id,
            'reason': 'dfdsdf'
        }
        response = self.client.post(url, data=report_data, follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertIn("There was an issue with the report.", str(messages_list[0]))

    def test_get_profile_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)