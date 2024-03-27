from random import randint
from peer_support.management.commands.helpers import get_user
from peer_support.management.commands.seeders.parent_seeder import parent_fixtures
from peer_support.management.commands.seeders.patient_seeder import patient_fixtures
from peer_support.models import Question, User

question_fixtures = [
    {
        "author": patient_fixtures[0],
        "title": "Question 1",
        "body": "This is my first question.",
    },
    {
        "author": parent_fixtures[0],
        "title": "Question 2",
        "body": "I have a question for you.",
    },
    {
        "author": patient_fixtures[1],
        "title": "Question 3",
        "body": "Can you help me with this?",
    },
    {
        "author": parent_fixtures[1],
        "title": "Question 4",
        "body": "I need help with something.",
    },
]

class QuestionSeeder:
    """Seed questions into the database."""

    QUESTION_COUNT = 250

    def __init__(self, faker):
        self.faker = faker
        self.users = User.objects.all()

    def create_questions(self):
        self.generate_question_fixtures()
        self.generate_random_questions()

    def generate_question_fixtures(self):
        for data in question_fixtures:
            self.try_create_question(data)

    def generate_random_questions(self):
        question_count = Question.objects.count()
        while question_count < self.QUESTION_COUNT:
            print(f"Seeding question {question_count}/{self.QUESTION_COUNT}", end="\r")
            self.generate_question()
            question_count = Question.objects.count()
        print("Question seeding complete.      ")

    def generate_question(self):
        author = self.users[randint(0, len(self.users) - 1)]
        title = self.faker.sentence()
        body = self.faker.text(max_nb_chars=500)
        author = {"username": author.username}
        self.try_create_question({"author": author, "title": title, "body": body})

    def try_create_question(self, data):
        try:
            self.create_question(data)
        except:
            pass

    def create_question(self, data):
        data["author"] = get_user(data["author"])
        Question.objects.create(**data)