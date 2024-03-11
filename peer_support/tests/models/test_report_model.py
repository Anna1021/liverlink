from django.test import TestCase
from peer_support.models import Report, Message, User
from django.contrib.contenttypes.models import ContentType

class ReportModelTest(TestCase):
    """Tests of the report view"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_message.json',
    ]


    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.message = Message.objects.first()

    def test_report_creation(self):
        report1 = Report.objects.create(
            reporter=self.user,
            reason='spam',
            content_object=self.message
        )
        self.assertEqual(report1.reason, 'spam')
        self.assertEqual(report1.reporter, self.user)
        self.assertEqual(report1.content_object, self.message)

        message_content_type = ContentType.objects.get_for_model(Message)
        self.assertEqual(report1.content_type, message_content_type)
        self.assertEqual(report1.object_id, self.message.id)

