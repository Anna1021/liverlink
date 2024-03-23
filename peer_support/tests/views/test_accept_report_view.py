"""Tests of the accept report view"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from peer_support.models import Report, Message, User, Post
from django.contrib.contenttypes.models import ContentType

class AcceptReportViewTestCase(TestCase):
    """Tests of the accept report view"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/default_message.json',
        'peer_support/tests/fixtures/default_post.json',
        'peer_support/tests/fixtures/default_report_message.json',
        'peer_support/tests/fixtures/default_report_user.json',
        'peer_support/tests/fixtures/default_report_post.json',
    ]
    
    def setUp(self):
        self.admin_user = User.objects.get(username='@admin')
        self.report_message = Report.objects.get(pk=1)
        self.report_user = Report.objects.get(pk=2)
        self.report_post = Report.objects.get(pk=4)
        message_content_type = ContentType.objects.get_for_model(Message)
        self.report_message.content_type = message_content_type
        self.report_message.save()
        user_content_type = ContentType.objects.get_for_model(User)
        self.report_user.content_type = user_content_type
        self.report_user.save()
        post_content_type = ContentType.objects.get_for_model(Post) 
        self.report_post.content_type = post_content_type
        self.report_post.save()
        self.url_message = reverse('accept_report', kwargs={'report_id':self.report_message.id})
        self.client.force_login(self.admin_user)
    
    def test_access_control_non_staff(self):
        self.client.logout()
        self.client.force_login(User.objects.get(username='@johndoe'))
        response = self.client.get(self.url_message)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('feed'))  
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
        self.message_to_report.delete(User.objects.all())
        response = self.client.get(self.url_message)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(["could not be found" in message.message for message in messages]))

    def test_successful_user_deactivation_by_staff(self):
        self.assertTrue(User.objects.filter(username='@janedoe').exists())
        url_user = reverse('accept_report', kwargs={'report_id':self.report_user.id})
        user_to_report = User.objects.get(pk =self.report_user.object_id)
        response = self.client.get(url_user)
        self.assertRedirects(response, reverse('moderation'))
        self.assertFalse(Report.objects.filter(pk=self.report_user.pk).exists())
        self.assertFalse(User.objects.get(pk=user_to_report.pk).is_active)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(["successfully deleted" in message.message for message in messages]))
    
    def test_successful_post_deletion_by_staff(self):
        post_to_report = Post.objects.get(pk=self.report_post.object_id)  
        self.assertTrue(Post.objects.filter(pk=post_to_report.pk).exists())
        url_post = reverse('accept_report', kwargs={'report_id':self.report_post.id})
        response = self.client.get(url_post)
        self.assertFalse(Post.objects.filter(pk=post_to_report.pk).exists())
        self.assertFalse(Report.objects.filter(pk=self.report_post.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(["successfully deleted" in str(message) for message in messages]))
        self.assertRedirects(response, reverse('moderation'))

