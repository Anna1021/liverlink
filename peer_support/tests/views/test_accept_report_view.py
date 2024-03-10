from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from peer_support.models import Report, Message, User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class AcceptReportViewTest(TestCase):
    """Tests of the accept report view"""

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
        message_content_type = ContentType.objects.get_for_model(self.message_to_report)
        self.report = Report.objects.create(
            reporter=self.admin_user,  
            reason='spam',  
            reported_at=timezone.now(),
            content_type=message_content_type,
            object_id=self.message_to_report.pk,
        )
        self.url = reverse('accept_report', kwargs={'report_id':self.report.id})
        self.client.force_login(self.admin_user)
    
    def test_access_control_non_staff(self):
        self.client.logout()
        self.client.force_login(User.objects.get(username='@johndoe'))
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('dashboard'))  
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have access to this view.")
    
    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/log_in/?next={self.url}')

    def test_successful_deletion_by_staff(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('moderation'))
        self.assertFalse(Report.objects.filter(pk=self.report.pk).exists())
        self.assertFalse(Message.objects.filter(content="Test message").exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(["successfully deleted" in message.message for message in messages]))

    def test_reported_object_not_found(self):
        self.report.content_object.delete(User.objects.all())
        response = self.client.get(self.url)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(["could not be found" in message.message for message in messages]))