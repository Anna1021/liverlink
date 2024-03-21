"""Unit tests for the reporting template tags"""
from django.test import TestCase
from peer_support.models import Question, Report, Post, User
from django.template import Context, Template
from django.contrib.contenttypes.models import ContentType

class ReportingTagsTestCase(TestCase):
    """Unit tests for the reporting template tags"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/default_question.json',
        'peer_support/tests/fixtures/default_post.json',
        'peer_support/tests/fixtures/default_report_question.json',
        'peer_support/tests/fixtures/default_report_user.json',
        'peer_support/tests/fixtures/default_report_post.json',
    ]

    def setUp(self):
        self.admin_user = User.objects.get(username='@admin') 
        self.report_post = Report.objects.get(pk=4)
        self.report_question = Report.objects.get(pk=5)
        self.report_user = Report.objects.get(pk=2)
        self.reported_question = Question.objects.get(pk=self.report_question.object_id)
        self.reported_post = Post.objects.get(pk=self.report_post.object_id)
        self.reported_user = User.objects.get(pk=self.report_user.object_id)

    def test_is_object_reported_by_user(self):
        template = Template(
            "{% load reporting_tags %}"
            "{{ object|is_object_reported_by_user:user }}"
        )
        context = Context({'object': self.reported_question, 'user': self.admin_user})
        rendered = template.render(context)
        print(rendered)
        self.assertIn("True", rendered)

    def test_display_reported_content_for_post(self):
        template = Template(
            "{% load reporting_tags %}"
            "{% display_reported_content report %}"
        )
        context = Context({'report': self.report_post})
        rendered = template.render(context)
        self.assertIn(self.reported_post.content, rendered)

    def test_display_reported_content_for_user(self):
        post_content_type = ContentType.objects.get_for_model(User)
        template = Template(
            "{% load reporting_tags %}"
            "{% display_reported_content report %}"
        )
        context = Context({'report': self.report_user})
        rendered = template.render(context)
        expected_link = f'href="/profile/{self.reported_user.username}/"'
        self.assertTrue(expected_link in rendered)
