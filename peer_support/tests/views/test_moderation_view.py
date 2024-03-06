from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from peer_support.models import Report
from django.contrib.messages import get_messages
from peer_support.tests.helpers import reverse_with_next

class ModerationViewTest(TestCase):

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/default_messages.json'
        'peer_support/tests/fixtures/default_report.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.force_login(self.user)
        self.url = reverse('moderation') 

    def test_get_moderation_redirects_when_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_access_control_non_staff(self):
        self.client.logout()
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