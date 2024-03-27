from django.core.management.base import BaseCommand
from faker import Faker
from peer_support.management.commands.seeders import *

class Command(BaseCommand):
    """Build automation command to seed the database."""

    help = "Seeds the database with sample data"

    def __init__(self):
        self.faker = Faker("en_GB")

    def handle(self, *args, **options):
        patient_seeder = PatientSeeder(self.faker)
        patient_seeder.create_patients()

        parent_seeder = ParentSeeder(self.faker)
        parent_seeder.create_parents()

        mentor_seeder = MentorSeeder(self.faker)
        mentor_seeder.create_mentors()

        professional_seeder = ProfessionalSeeder(self.faker)
        professional_seeder.create_professionals()

        user_seeder = UserSeeder(self.faker)
        user_seeder.seed_friends()
        user_seeder.seed_blocked_users()
        
        post_seeder = PostSeeder(self.faker)
        post_seeder.create_posts()

        post_comment_seeder = PostCommentSeeder(self.faker)
        post_comment_seeder.create_post_comments()

        question_seeder = QuestionSeeder(self.faker)
        question_seeder.create_questions()

        response_seeder = ResponseSeeder(self.faker)
        response_seeder.create_responses()

        conversation_and_message_seeder = ConversationAndMessageSeeder(self.faker)
        conversation_and_message_seeder.create_conversations()

        report_seeder = ReportSeeder(self.faker)
        report_seeder.create_reports()

        feedback_seeder = FeedbackSeeder(self.faker)
        feedback_seeder.create_feedbacks()

        friend_request_seeder = FriendRequestSeeder(self.faker)
        friend_request_seeder.create_friend_requests()

        notification_seeder = NotificationSeeder(self.faker)
        notification_seeder.create_notifications()