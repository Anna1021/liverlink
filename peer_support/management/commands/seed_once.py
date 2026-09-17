from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

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


class Command(BaseCommand):
    """Seed demo data once, and safely skip subsequent application starts."""

    help = "Seeds missing demo data and skips when the complete demo dataset exists"

    targets = (
        (Patient, 100),
        (Parent, 100),
        (Mentor, 100),
        (Professional, 100),
        (Post, 500),
        (PostComment, 1000),
        (Question, 250),
        (Response, 1000),
        (Conversation, 500),
        (Report, 500),
        (Feedback, 500),
        (FriendRequest, 100),
        (Notification, 500),
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
        with transaction.atomic():
            call_command("seed")
        self.stdout.write(self.style.SUCCESS("Demo data seeding complete."))
