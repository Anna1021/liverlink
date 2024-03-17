"""Unit test of report form"""
from django.test import TestCase
from peer_support.models import Report, Message, User
from peer_support.forms import ReportForm
from django.contrib.contenttypes.models import ContentType

class ReportFormTestCase(TestCase):
    """Unit test of report form"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/default_message.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.object_to_report = Message.objects.first()
        self.form_data = {'reason': 'spam'} 

    def test_form_validation(self):
        form = ReportForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_save_report_for_object(self):
        form = ReportForm(data=self.form_data)
        if form.is_valid():
            report = form.save_report_for_object(self.object_to_report, self.user)
            self.assertIsInstance(report, Report)
            self.assertEqual(report.reason, self.form_data['reason'])
            self.assertEqual(report.reporter, self.user)
            self.assertEqual(report.content_type, ContentType.objects.get_for_model(self.object_to_report))
            self.assertEqual(report.object_id, self.object_to_report.pk)
        else:
            self.fail("Form did not validate")

    def test_invalid_form_save_attempt(self):
        invalid_form_data = {}
        form = ReportForm(data=invalid_form_data)
        with self.assertRaises(ValueError):
            form.save_report_for_object(self.object_to_report, self.user)
