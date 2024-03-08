from django.test import TestCase
from django.urls import reverse
from peer_support.forms import FilterPeerForm, SortPeerForm, SearchPeerForm
from peer_support.models import User
from peer_support.tests.helpers import reverse_with_next
from django.utils.http import urlencode
from django.contrib.messages import get_messages
from peer_support.models import Report, User, Message
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class ModerationViewTestCase(TestCase):
    """Tests of the moderation view."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/default_message.json',
    ]

    def setUp(self):
        self.url = reverse('moderation')
        self.admin_user = User.objects.get(username='@admin')
        message_to_report = Message.objects.first() 
        message_content_type = ContentType.objects.get_for_model(message_to_report)
        self.report = Report.objects.create(
            reporter=self.admin_user,  
            reason='spam',  
            reported_at=timezone.now(),
            content_type=message_content_type,
            object_id=message_to_report.pk,
        )
        self.client.force_login(self.admin_user)

    def test_get_moderation_redirects_when_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_access_control_non_staff(self):
        self.client.logout()
        self.client.force_login(User.objects.get(username='@johndoe'))
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('dashboard'))  
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have access to this view.")

    def test_access_control_staff(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderation.html')

    def test_reports_listing_for_staff(self):
        response = self.client.get(self.url)
        self.assertTrue('reports' in response.context)
        self.assertEqual(len(response.context['reports']), 1)
