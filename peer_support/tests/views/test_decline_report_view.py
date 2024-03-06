from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from peer_support.models import Report, Message, User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class DeclineReportViewTest(TestCase):

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
        self.url = reverse('decline_report', kwargs={'report_id':self.report.id})
        self.client.force_login(self.admin_user)

    def test_decline_report(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('moderation'), status_code=302, target_status_code=200)
        with self.assertRaises(Report.DoesNotExist):
            Report.objects.get(pk=self.report.pk)
        self.assertIn(self.report.reporter, self.message_to_report.visible_to.all())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Report and the reported object have been successfully deleted.")

    def test_access_control_non_staff(self):
        self.client.logout()
        self.client.force_login(User.objects.get(username='@johndoe'))
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('dashboard'))  
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have access to this view.")
