from random import randint
import uuid
from peer_support.forms.form_choices import CONDITION_CHOICES, TRANSPLANT_CHOICES
from peer_support.management.commands.seeders.user_seeder import UserSeeder
from peer_support.models import Mentor

mentor_fixtures = [
    {
        "username": "@sarahsmith",
        "email": "sarah.smith@example.org",
        "first_name": "Sarah",
        "last_name": "Smith",
        "date_of_birth": "1992-05-15",
        "gender": "F",
        "location": "GB",
        "hospital": "Blackpool Teaching Hospitals NHS Foundation Trust",
        "ethnicity": "BR",
        "language": "en",
        "bio": "Hello, I am Sarah.",
        "condition": "Diabetes",
        "age_of_diagnosis": 7,
        "referral_code": "ABC123",
    },
    {
        "username": "@davidbrown",
        "email": "david.brown@example.org",
        "first_name": "David",
        "last_name": "Brown",
        "date_of_birth": "1985-09-20",
        "gender": "M",
        "location": "GB",
        "hospital": "Countess of Chester Hospital NHS Foundation Trust",
        "ethnicity": "BR",
        "language": "en",
        "bio": "Hey there, I am David.",
        "age_of_diagnosis": 8,
        "referral_code": "DEF456",
    },
    {
        "username": "@emilywilson",
        "email": "emily.wilson@example.org",
        "first_name": "Emily",
        "last_name": "Wilson",
        "date_of_birth": "1978-12-03",
        "gender": "F",
        "location": "AU",
        "ethnicity": "BR",
        "language": "en",
        "bio": "Hi, I am Emily.",
        "age_of_diagnosis": 3,
        "referral_code": "GHI789",
    },
]

class MentorSeeder:
    """Seed mentors into the database."""

    MENTOR_COUNT = 100

    def __init__(self, faker):
        self.faker = faker
        self.user_seeder = UserSeeder(self.faker)

    def create_mentors(self):
        self.generate_mentor_fixtures()
        self.generate_random_mentors()

    def generate_mentor_fixtures(self):
        for data in mentor_fixtures:
            self.try_create_mentor(data)
    
    def generate_random_mentors(self):
        mentor_count = Mentor.objects.count()
        while mentor_count < self.MENTOR_COUNT:
            print(f"Seeding mentor {mentor_count}/{self.MENTOR_COUNT}", end="\r")
            self.generate_mentor()
            mentor_count = Mentor.objects.count()
        print("Mentor seeding complete.      ")

    def generate_mentor(self):
        user_data = self.user_seeder.generate_user_data()
        condition = self.faker.random_element(elements=(tuple(condition[0] for condition in CONDITION_CHOICES)))
        age_of_diagnosis = randint(0, 30)
        referral_code = uuid.uuid4().hex[:10].upper()
        transplant = self.faker.random_element(elements=(tuple(transplant[0] for transplant in TRANSPLANT_CHOICES)))
        user_data.update({'condition': condition, 'age_of_diagnosis': age_of_diagnosis, 'referral_code': referral_code, 'transplant': transplant})
        self.try_create_mentor(user_data)

    def try_create_mentor(self, data):
        try:
            self.create_mentor(data)
        except:
            pass

    def create_mentor(self, data):
        self.user_seeder.create_user(Mentor, data)
    
