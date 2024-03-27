from peer_support.models import Feedback, User

feedback_fixtures = [
    {"title": "Fix this", "content": "This is broken."},
    {"title": "Improve that", "content": "This could be improved"},
    {"title": "Add this", "content": "This is missing."},
]

class FeedbackSeeder:
    """Seed feedback into the database."""

    FEEDBACK_COUNT = 500

    def __init__(self, faker):
        self.faker = faker

    def create_feedbacks(self):
        self.generate_feedback_fixtures()
        self.generate_random_feedbacks()

    def generate_feedback_fixtures(self):
        for data in feedback_fixtures:
            self.try_create_feedback(data)

    def generate_random_feedbacks(self):
        feedback_count = Feedback.objects.count()
        while feedback_count < self.FEEDBACK_COUNT:
            print(f"Seeding feedback {feedback_count}/{self.FEEDBACK_COUNT}", end="\r")
            self.generate_feedback()
            feedback_count = Feedback.objects.count()
        print("Feedback seeding complete.      ")

    def generate_feedback(self):
        title = self.faker.sentence()
        content = self.faker.text(max_nb_chars=500)
        self.try_create_feedback({"title": title, "content": content})

    def try_create_feedback(self, data):
        try:
            self.create_feedback(data)
        except:
            pass

    def create_feedback(self, data):
        Feedback.objects.create(**data)
        