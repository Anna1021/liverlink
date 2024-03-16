"""Tests of the profile view"""
from django.test import TestCase
from django.urls import reverse
from peer_support.models import Report, User, Conversation, GroupConversation, FriendRequest
from peer_support.forms import ReportForm
from django.contrib.contenttypes.models import ContentType
from peer_support.tests.helpers import reverse_with_next
from django.contrib import messages
from django.contrib.messages import get_messages

class ProfileViewTest(TestCase):
    """Tests of the profile view"""

    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/default_admin.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/default_parent.json',
                'peer_support/tests/fixtures/other_patients.json',
                'peer_support/tests/fixtures/other_mentors.json',
                'peer_support/tests/fixtures/default_report_user.json',
            ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.report_user = Report.objects.get(pk=2)
        self.user_to_report = User.objects.get(pk =self.report_user.object_id)
        self.user_to_message = User.objects.get(username='@janedoe')
        self.url_report = reverse('profile', kwargs={'username':self.user_to_report})
        self.url = reverse('profile',kwargs={'username':self.user.username})
        self.client.force_login(self.user)
    
    def test_successful_report_profile(self):
        report_data = {
            'report': 'report',
            'action': self.user_to_report.pk,
            'reason': 'abuse'
        }
        response = self.client.post(self.url_report, data=report_data)
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
            'report': 'report',
            'action': valid_message_id,
            'reason': 'dfdsdf'
        }
        response = self.client.post(self.url_report, data=report_data, follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertIn("There was an issue with the report.", str(messages_list[0]))

    def test_report_profile_with_missing_form_name_has_no_effect(self):
        before_count = Report.objects.count()
        report_data = {
            'action': self.user_to_report.pk,
            'reason': 'abuse'
        }
        response = self.client.post(self.url_report, data=report_data, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count = Report.objects.count()
        self.assertEqual(before_count, after_count)

    def test_get_conversation_with_missing_form_name_has_no_effect(self):
        before_count = Conversation.objects.count()
        conversation_data = {
            'users': [self.user_to_message.id]
        }
        response = self.client.post(self.url, data=conversation_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1][0], self.url)
        after_count = Conversation.objects.count()
        self.assertEqual(before_count, after_count)

    def test_get_conversation_when_no_conversation_exists_creates_conversation(self):
        self.assertEqual(Conversation.objects.count(), 0)
        conversation_data = {
            'message': 'message',
            'users': [self.user_to_message.id]
        }
        response = self.client.post(self.url, data=conversation_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Conversation.objects.count(), 1)
        conversation = Conversation.objects.first()
        redirect_url = reverse('conversation', kwargs={'conversation_id': conversation.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertIn(self.user, conversation.users.all())
        self.assertIn(self.user_to_message, conversation.users.all())
        self.assertEqual(2, conversation.users.count())
        self.assertIsNone(conversation.as_group())
        self.assertIn(conversation, self.user.conversations.all())
        self.assertIn(conversation, self.user_to_message.conversations.all())

    def test_get_conversation_when_no_direct_conversation_exists_creates_conversation(self):
        groupchat = GroupConversation.objects.create()
        groupchat.users.add(self.user)
        groupchat.users.add(self.user_to_message)
        self.assertIsNotNone(groupchat.as_group())
        self.assertEqual(Conversation.objects.count(), 1)
        conversation_data = {
            'message': 'message',
            'users': [self.user_to_message.id]
        }
        response = self.client.post(self.url, data=conversation_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Conversation.objects.count(), 2)
        conversation = Conversation.objects.last()
        redirect_url = reverse('conversation', kwargs={'conversation_id': conversation.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertNotEqual(groupchat, conversation)
        self.assertIn(self.user, conversation.users.all())
        self.assertIn(self.user_to_message, conversation.users.all())
        self.assertEqual(2, conversation.users.count())
        self.assertIsNone(conversation.as_group())
        self.assertIn(conversation, self.user.conversations.all())
        self.assertIn(conversation, self.user_to_message.conversations.all())

    def test_get_conversation_when_conversation_exists(self):
        conv = Conversation.objects.create()
        conv.users.add(self.user)
        conv.users.add(self.user_to_message)
        self.user.conversations.add(conv)
        self.user_to_message.conversations.add(conv)
        self.assertIsNone(conv.as_group())
        self.assertEqual(Conversation.objects.count(), 1)
        conversation_data = {
            'message': 'message',
            'users': [self.user_to_message.id]
        }
        response = self.client.post(self.url, data=conversation_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Conversation.objects.count(), 1)
        conversation = Conversation.objects.first()
        redirect_url = reverse('conversation', kwargs={'conversation_id': conversation.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertEqual(conv, conversation)
        self.assertIn(self.user, conversation.users.all())
        self.assertIn(self.user_to_message, conversation.users.all())
        self.assertEqual(2, conversation.users.count())
        self.assertIsNone(conversation.as_group())
        self.assertIn(conversation, self.user.conversations.all())
        self.assertIn(conversation, self.user_to_message.conversations.all())

    def test_profile_url(self):
        self.assertEqual(self.url,'/profile/@johndoe/')

    def test_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        user = response.context['user']
        self.assertEqual(user, self.user)
        report_form = response.context['report_form']
        self.assertIsInstance(report_form, ReportForm)

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
        parent = response.context['user_type']
        self.assertEqual(parent, "PARENT")

    def test_get_profile_admin(self):
        user = User.objects.get(username='@admin')
        url = reverse('profile', kwargs={'username': user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        admin = response.context['user_type']
        self.assertEqual(admin, "ADMIN")

    def test_get_profile_patient(self):
        user = User.objects.get(username='@janedoe')
        url = reverse('profile', kwargs={'username': user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        patient = response.context['user_type']
        self.assertEqual(patient, "PATIENT")

    def test_get_profile_mentor(self):
        user = User.objects.get(username='@alexsmith')
        url = reverse('profile', kwargs={'username': user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        mentor = response.context['user_type']
        self.assertEqual(mentor, "MENTOR")

    def test_get_profile_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url)

    def test_non_existent_profile_redirect(self):
        non_existent_username = 'noonehere'
        url = reverse('profile', kwargs={'username': non_existent_username})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('dashboard'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(["does not exist" in str(message) for message in messages]))