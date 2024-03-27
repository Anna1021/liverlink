import uuid
from peer_support.forms.form_choices import CONDITION_CHOICES
from peer_support.management.commands.seeders.user_seeder import UserSeeder
from peer_support.models import Professional

professional_fixtures = [
    {
        "username": "@joanneclarke",
        "email": "joanne.clarke@example.org",
        "first_name": "Joanne",
        "last_name": "Clarke",
        "date_of_birth": "1968-04-15",
        "gender": "F",
        "location": "US",
        "ethnicity": "BR",
        "language": "en",
        "bio": "Hello, I am Joanne.",
        "expertise": "Diabetes",
        "referral_code": "ABC123",
    },
    {
        "username": "@jeremybarnett",
        "email": "jeremny.barnett@example.org",
        "first_name": "Jeremy",
        "last_name": "Barnett",
        "date_of_birth": "1995-11-02",
        "gender": "M",
        "location": "CA",
        "ethnicity": "BR",
        "language": "en",
        "bio": "Hey there, I am Jeremy.",
        "referral_code": "DEF456",
    },
    {
        "username": "@paulaevans",
        "email": "paula.evans@example.org",
        "first_name": "Paula",
        "last_name": "Evans",
        "date_of_birth": "1975-2-30",
        "gender": "F",
        "location": "AU",
        "ethnicity": "BR",
        "language": "en",
        "bio": "Hi, I am Paula.",
        "referral_code": "GHI789",
    },
]


class ProfessionalSeeder:
    """Seed professionals into the database."""

    PROFESSIONAL_COUNT = 100

    def __init__(self, faker):
        self.faker = faker
        self.user_seeder = UserSeeder(self.faker)

    def create_professionals(self):
        self.generate_professional_fixtures()
        self.generate_random_professionals()

    def generate_professional_fixtures(self):
        for data in professional_fixtures:
            self.try_create_professional(data)

    def generate_random_professionals(self):
        professional_count = Professional.objects.count()
        while professional_count < self.PROFESSIONAL_COUNT:
            print(f"Seeding professional {professional_count}/{self.PROFESSIONAL_COUNT}", end='\r')
            self.generate_professional()
            professional_count = Professional.objects.count()
        print("Professional seeding complete.      ")

    def generate_professional(self):
        user_data = self.user_seeder.generate_user_data()
        expertise = self.faker.random_element(elements=(tuple(condition[0] for condition in CONDITION_CHOICES)))
        referral_code = uuid.uuid4().hex[:10].upper()
        user_data.update({'expertise': expertise, 'referral_code': referral_code})
        self.try_create_professional(user_data)

    def try_create_professional(self, data):
        try:
            self.create_professional(data)
        except:
            pass

    def create_professional(self, data):
        self.user_seeder.create_user(Professional, data)

    