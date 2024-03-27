from random import randint
from peer_support.management.commands.helpers import get_user, get_content_type, get_message
from peer_support.management.commands.seeders.parent_seeder import parent_fixtures
from peer_support.management.commands.seeders.patient_seeder import patient_fixtures
from peer_support.management.commands.seeders.conversation_and_message_seeder import message_fixtures
from peer_support.models.model_choices import REPORT_CHOICES
from peer_support.models import Report, User

report_fixtures = [
    {
        "reporter": patient_fixtures[0],
        "reason": "abuse",
        "content_type": "User",
        "object_id": patient_fixtures[1],
    },
    {
        "reporter": parent_fixtures[0],
        "reason": "other",
        "content_type": "Message",
        "object_id": message_fixtures[0],
    },
    {
        "reporter": patient_fixtures[2],
        "reason": "spam",
        "content_type": "User",
        "object_id": parent_fixtures[0],
    },
]

class ReportSeeder:
    """Seed reports into the database."""

    REPORT_COUNT = 500

    def __init__(self, faker):
        self.faker = faker
        self.users = User.objects.all()

    def create_reports(self):
        self.generate_report_fixtures()
        self.generate_random_reports()

    def generate_report_fixtures(self):
        for data in report_fixtures:
            self.try_create_report(data)

    def generate_random_reports(self):
        report_count = Report.objects.count()
        while report_count < self.REPORT_COUNT:
            print(f"Seeding report {report_count}/{self.REPORT_COUNT}", end="\r")
            self.generate_report()
            report_count = Report.objects.count()
        print("Report seeding complete.      ")

    def generate_report(self):
        reporter = self.users[randint(0, len(self.users) - 1)]
        reason = self.faker.random_element(elements=(tuple(report[0] for report in REPORT_CHOICES)))
        content_type = self.faker.random_element(elements=("user", "message"))
        object_id = (get_content_type(content_type)
            .model_class()
            .objects.order_by("?")
            .first()
            .pk
        )
        reporter = {"username": reporter.username}
        self.try_create_report({"reporter": reporter, "reason": reason,  "content_type": content_type, "object_id": object_id})

    def try_create_report(self, data):
        try:
            self.create_report(data)
        except:
            pass

    def create_report(self, data):
        data["reporter"] = get_user(data["reporter"])
        if data["content_type"] == "User":
            data["object_id"] = get_user(data["object_id"]).pk
        elif data["content_type"] == "Message":
            data["object_id"] = get_message(data["object_id"]).pk
        data["content_type"] = get_content_type(data["content_type"].lower())
        Report.objects.create(**data)