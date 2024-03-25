"""Tests of the decline report view"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from peer_support.models import Report, Message, User
from django.contrib.contenttypes.models import ContentType

from django.contrib.contenttypes.models import ContentType

class DeclineReportViewTestCase(TestCase):
    """Tests of the decline report view"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/default_message.json',
        'peer_support/tests/fixtures/default_report_message.json',
        'peer_support/tests/fixtures/default_report_user.json',
    ]

    def setUp(self):
        self.admin_user = User.objects.get(username='@admin')
        self.message_to_report = Message.objects.first() 
        self.report_message = Report.objects.get(pk=1)
        message_content_type = ContentType.objects.get_for_model(Message)
        self.report_message.content_type = message_content_type
        self.report_message.save()
        self.report_user = Report.objects.get(pk=2)
        user_content_type = ContentType.objects.get_for_model(User)
        self.report_user.content_type = user_content_type
        self.report_user.save()
        self.message_to_report = Message.objects.get(pk=self.report_message.object_id)
        self.user_to_report = User.objects.get(pk=self.report_user.object_id)
        self.url_message = reverse('decline_report', kwargs={'report_id':self.report_message.id})
        self.url_user = reverse('decline_report', kwargs={'report_id':self.report_user.id})
        self.client.force_login(self.admin_user)

    def test_decline_report_message(self):
        response = self.client.get(self.url_message)
        self.assertRedirects(response, reverse('moderation'), status_code=302, target_status_code=200)
        with self.assertRaises(Report.DoesNotExist):
            Report.objects.get(pk=self.report_message.pk)
        self.assertIn(self.report_message.reporter, self.message_to_report.visible_to.all())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Report has been successfully deleted.")

    def test_access_control_non_staff(self):
        self.client.logout()
        self.client.force_login(User.objects.get(username='@johndoe'))
        response = self.client.get(self.url_message)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('feed'))  
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have access to this view.")

    def test_reported_object_not_found(self):
        self.report_message.content_object.delete(User.objects.all())
        response = self.client.get(self.url_message)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(["could not be found" in message.message for message in messages]))

    def test_decline_report_user(self):
        response = self.client.get(self.url_user)
        self.assertRedirects(response, reverse('moderation'), status_code=302, target_status_code=200)
        with self.assertRaises(Report.DoesNotExist):
            Report.objects.get(pk=self.report_user.pk)
        self.assertTrue(User.objects.get(pk=self.user_to_report.pk).is_active)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Report has been successfully deleted.")