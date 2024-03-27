from random import randint
from peer_support.management.commands.helpers import get_user
from peer_support.management.commands.seeders.parent_seeder import parent_fixtures
from peer_support.management.commands.seeders.mentor_seeder import mentor_fixtures
from peer_support.management.commands.seeders.question_seeder import question_fixtures
from peer_support.models import Response, User, Question

response_fixtures = [
    {
        "user": mentor_fixtures[0],
        "question": question_fixtures[0],
        "body": "This is my first response.",
    },
    {
        "user": mentor_fixtures[1],
        "question": question_fixtures[1],
        "body": "I have a response for you.",
    },
    {
        "user": mentor_fixtures[2],
        "question": question_fixtures[2],
        "body": "I can help you with this.",
    },
    {
        "user": parent_fixtures[0],
        "question": question_fixtures[3],
        "body": "I can help you.",
    },
]

class ResponseSeeder:
    """Seed responses into the database."""

    RESPONSE_COUNT = 1000

    def __init__(self, faker):
        self.faker = faker
        self.users = User.objects.all()
        self.questions = Question.objects.all()

    def create_responses(self):
        self.generate_response_fixtures()
        self.generate_random_responses()

    def generate_response_fixtures(self):
        for data in response_fixtures:
            self.try_create_response(data)

    def generate_random_responses(self):
        response_count = Response.objects.count()
        while response_count < self.RESPONSE_COUNT:
            print(f"Seeding response {response_count}/{self.RESPONSE_COUNT}", end="\r")
            self.generate_response()
            response_count = Response.objects.count()
        print("Response seeding complete.      ")

    def generate_response(self):
        user = self.users[randint(0, len(self.users) - 1)]
        question = self.questions[randint(0, len(self.questions) - 1)]
        body = self.faker.text(max_nb_chars=300)
        user = {"username": user.username}
        question = {"title": question.title}
        self.try_create_response({"user": user, "question": question, "body": body})

    def try_create_response(self, data):
        try:
            self.create_response(data)
        except:
            pass

    def create_response(self, data):
        data["user"] = get_user(data["user"])
        data["question"] = Question.objects.filter(
            title=data["question"]["title"]
        ).first()
        Response.objects.create(**data)