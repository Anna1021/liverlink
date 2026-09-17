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
        (Patient, 20),
        (Parent, 20),
        (Mentor, 20),
        (Professional, 20),
        (Post, 100),
        (PostComment, 200),
        (Question, 50),
        (Response, 200),
        (Conversation, 100),
        (Report, 100),
        (Feedback, 100),
        (FriendRequest, 20),
        (Notification, 100),
    )

    seeders = (
        (PatientSeeder, "PATIENT_COUNT", 20),
        (ParentSeeder, "PARENT_COUNT", 20),
        (MentorSeeder, "MENTOR_COUNT", 20),
        (ProfessionalSeeder, "PROFESSIONAL_COUNT", 20),
        (PostSeeder, "POST_COUNT", 100),
        (PostCommentSeeder, "POST_COMMENT_COUNT", 200),
        (QuestionSeeder, "QUESTION_COUNT", 50),
        (ResponseSeeder, "RESPONSE_COUNT", 200),
        (ConversationAndMessageSeeder, "CONVERSATION_COUNT", 100),
        (ReportSeeder, "REPORT_COUNT", 100),
        (FeedbackSeeder, "FEEDBACK_COUNT", 100),
        (FriendRequestSeeder, "FRIEND_REQUEST_COUNT", 20),
        (NotificationSeeder, "NOTIFICATION_COUNT", 100),
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
