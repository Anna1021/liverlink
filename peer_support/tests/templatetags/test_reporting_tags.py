"""Unit tests for the reporting template tags"""
from django.test import TestCase
from django.contrib.auth.models import User
from peer_support.models import Question, Report, Post
from django.template import Context, Template
from django.contrib.contenttypes.models import ContentType

class ReportingTagsTestCase(TestCase):
    """Unit tests for the reporting template tags"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/default_question.json',
        'peer_support/tests/fixtures/default_post.json',
        'peer_support/tests/fixtures/default_report_question.json',
        'peer_support/tests/fixtures/default_report_user.json',
        'peer_support/tests/fixtures/default_report_post.json',
    ]

    def setUp(self):
        user_content_type = ContentType.objects.get_for_model(User)
        post_content_type = ContentType.objects.get_for_model(Post)
        question_content_type = ContentType.objects.get_for_model(Question) 
        self.report_user = Report.objects.filter(content_type=user_content_type).first()
        self.report_post = Report.objects.filter(content_type=post_content_type).first()
        self.report_question = Report.objects.filter(content_type=question_content_type).first()
        self.user = User.objects.get(username='@admin') 
        self.report_question = Question.objects.get(pk=self.report_question.object_id)
        self.reported_post = Post.objects.get(pk=self.report_post.object_id)
        self.reported_question = Question.objects.get(pk=self.report_question.object_id)

    def test_is_object_reported_by_user(self):
        template = Template(
            "{% load reporting_tags %}"
            "{{ object|is_object_reported_by_user:user }}"
        )
        context = Context({'object': self.reported_message, 'user': self.user})
        rendered = template.render(context)
        self.assertIn("True", rendered)

    def test_display_reported_content_for_message(self):
        template = Template(
            "{% load reporting_tags %}"
            "{% display_reported_content report %}"
        )
        context = Context({'report': self.report})
        rendered = template.render(context)
        self.assertIn(self.reported_message.content, rendered)

    def test_display_reported_content_for_user(self):
        user_report = Report.objects.create(
            content_object=self.reported_user,
            reporter=self.user,
            reason="Test reason for reporting user."
        )
        template = Template(
            "{% load reporting_tags %}"
            "{% display_reported_content report %}"
        )
        context = Context({'report': user_report})
        rendered = template.render(context)
        self.assertTrue(f'href="/profile/{self.reported_user.username}"' in rendered)