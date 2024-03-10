from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from peer_support.models import Report, Message, User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class DeclineReportViewTest(TestCase):
    """Tests of the decline report view"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/default_message.json',
    ]

    def setUp(self):
        self.admin_user = User.objects.get(username='@admin')
        self.message_to_report = Message.objects.first() 
        self.user_to_report = User.objects.get(username='@janedoe')
        self.user_to_report.is_active = True
        self.user_to_report.save()
        message_content_type = ContentType.objects.get_for_model(self.message_to_report)
        user_content_type = ContentType.objects.get_for_model(self.message_to_report)
        self.report_message = Report.objects.create(
            reporter=self.admin_user,  
            reason='spam',  
            reported_at=timezone.now(),
            content_type=message_content_type,
            object_id=self.message_to_report.pk,
        )
        self.report_user = Report.objects.create(
            reporter=self.admin_user,  
            reason='spam',  
            reported_at=timezone.now(),
            content_type=user_content_type,
            object_id=self.user_to_report.pk,
            content_object=self.user_to_report,
        )
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
        self.assertEqual(str(messages[0]), "Report and the reported object have been successfully deleted.")

    def test_access_control_non_staff(self):
        self.client.logout()
        self.client.force_login(User.objects.get(username='@johndoe'))
        response = self.client.get(self.url_message)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('dashboard'))  
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
        self.assertEqual(str(messages[0]), "Report and the reported object have been successfully deleted.")