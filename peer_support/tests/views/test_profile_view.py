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
