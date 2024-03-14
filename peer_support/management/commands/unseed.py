from django.core.management.base import BaseCommand
from peer_support.models import *

class Command(BaseCommand):
    """Build automation command to unseed the database."""
    
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        """Unseed the database."""

        Conversation.objects.all().delete()
        FriendRequest.objects.all().delete()
        GroupConversation.objects.all().delete()
        Message.objects.all().delete()
        Notification.objects.all().delete()
        Question.objects.all().delete()
        Report.objects.all().delete()
        Response.objects.all().delete()
        User.objects.filter(is_staff=False).delete()
        