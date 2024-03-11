from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from peer_support.models import Report, Message, User

class AcceptReportViewTestCase(TestCase):
    """Tests of the accept report view"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/default_message.json',
        'peer_support/tests/fixtures/other_reports_message.json',
        'peer_support/tests/fixtures/other_reports_user.json',
    ]
    
    def setUp(self):
        self.admin_user = User.objects.get(username='@admin')
        self.report_message = Report.objects.get(pk=1)
        self.report_user = Report.objects.get(pk=2)
        self.message_to_report = Message.objects.get(pk=self.report_message.object_id)
        self.user_to_report = User.objects.get(pk =self.report_user.object_id)
        self.url_message = reverse('accept_report', kwargs={'report_id':self.report_message.id})
        self.url_user = reverse('accept_report', kwargs={'report_id':self.report_user.id})
        self.client.force_login(self.admin_user)
    
    def test_access_control_non_staff(self):
        self.client.logout()
        self.client.force_login(User.objects.get(username='@johndoe'))
        response = self.client.get(self.url_message)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('dashboard'))  
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have access to this view.")
    
    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url_message)
        self.assertRedirects(response, f'/log_in/?next={self.url_message}')

    def test_successful_message_deletion_by_staff(self):
        response = self.client.get(self.url_message)
        self.assertRedirects(response, reverse('moderation'))
        self.assertFalse(Report.objects.filter(pk=self.report_message.pk).exists())
        self.assertFalse(Message.objects.filter(content="Test message").exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(["successfully deleted" in message.message for message in messages]))

    def test_reported_object_not_found(self):
        self.report_message.content_object.delete(User.objects.all())
        response = self.client.get(self.url_message)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(["could not be found" in message.message for message in messages]))

    def test_successful_user_deactivation_by_staff(self):
        self.assertTrue(User.objects.filter(username='@janedoe').exists())
        response = self.client.get(self.url_user)
        self.assertRedirects(response, reverse('moderation'))
        self.assertFalse(Report.objects.filter(pk=self.report_user.pk).exists())
        self.assertFalse(User.objects.get(pk=self.user_to_report.pk).is_active)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(["successfully deleted" in message.message for message in messages]))