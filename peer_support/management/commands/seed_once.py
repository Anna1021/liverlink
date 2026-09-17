from django.core.management import call_command
from django.core.management.base import BaseCommand

from peer_support.models import (
    Conversation,
    Feedback,
    FriendRequest,
    Mentor,
    Notification,
    Parent,
    Patient,
    Post,
    PostComment,
    Professional,
    Question,
    Report,
    Response,
)
from peer_support.management.commands.seeders import (
    ConversationAndMessageSeeder,
    FeedbackSeeder,
    FriendRequestSeeder,
    MentorSeeder,
    NotificationSeeder,
    ParentSeeder,
    PatientSeeder,
    PostCommentSeeder,
    PostSeeder,
    ProfessionalSeeder,
    QuestionSeeder,
    ReportSeeder,
    ResponseSeeder,
)


class Command(BaseCommand):
    """Seed demo data once, and safely skip subsequent application starts."""

    help = "Seeds missing demo data and skips when the complete demo dataset exists"

    targets = (
        (Patient, 25),
        (Parent, 25),
        (Mentor, 25),
        (Professional, 25),
        (Post, 50),
        (PostComment, 100),
        (Question, 30),
        (Response, 100),
        (Conversation, 30),
        (Report, 30),
        (Feedback, 30),
        (FriendRequest, 20),
        (Notification, 50),
    )

    seeders = (
        (PatientSeeder, "PATIENT_COUNT", 25),
        (ParentSeeder, "PARENT_COUNT", 25),
        (MentorSeeder, "MENTOR_COUNT", 25),
        (ProfessionalSeeder, "PROFESSIONAL_COUNT", 25),
        (PostSeeder, "POST_COUNT", 50),
        (PostCommentSeeder, "POST_COMMENT_COUNT", 100),
        (QuestionSeeder, "QUESTION_COUNT", 30),
        (ResponseSeeder, "RESPONSE_COUNT", 100),
        (ConversationAndMessageSeeder, "CONVERSATION_COUNT", 30),
        (ReportSeeder, "REPORT_COUNT", 30),
        (FeedbackSeeder, "FEEDBACK_COUNT", 30),
        (FriendRequestSeeder, "FRIEND_REQUEST_COUNT", 20),
        (NotificationSeeder, "NOTIFICATION_COUNT", 50),
    )

    def handle(self, *args, **options):
        missing = [
            f"{model.__name__} ({model.objects.count()}/{target})"
            for model, target in self.targets
            if model.objects.count() < target
        ]
        if not missing:
            self.stdout.write(self.style.SUCCESS("Demo data already seeded; skipping."))
            return

        self.stdout.write("Seeding missing demo data: " + ", ".join(missing))
        for seeder, attribute, target in self.seeders:
            setattr(seeder, attribute, target)
        call_command("seed")
        self.stdout.write(self.style.SUCCESS("Demo data seeding complete."))
