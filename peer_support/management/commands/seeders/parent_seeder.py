from random import randint
from peer_support.forms.form_choices import CONDITION_CHOICES, TRANSPLANT_CHOICES
from peer_support.management.commands.seeders.user_seeder import UserSeeder
from peer_support.models import Parent

parent_fixtures = [
    {
        "username": "@jackjones",
        "email": "jack.jones@example.org",
        "first_name": "Jack",
        "last_name": "Jones",
        "date_of_birth": "1980-01-01",
        "gender": "M",
        "location": "GB",
        "hospital": "Croydon Health Services NHS Trust",
        "ethnicity": "BR",
        "language": "en",
        "bio": "Hi, I am Jack.",
        "child_condition": "Diabetes",
        "child_age_of_diagnosis": 5,
    },
    {
        "username": "@jilljones",
        "email": "jill.jones@example.org",
        "first_name": "Jill",
        "last_name": "Jones",
        "date_of_birth": "1985-04-20",
        "gender": "F",
        "location": "FR",
        "ethnicity": "RO",
        "language": "fr",
        "bio": "Hi, I am Jill.",
        "child_condition": "Hepatitis A",
        "child_age_of_diagnosis": 10,
    },
    {
        "username": "@danielcaesar",
        "email": "daniel.caesar@example.org",
        "first_name": "Daniel",
        "last_name": "Caesar",
        "date_of_birth": "1992-03-02",
        "gender": "O",
        "location": "BD",
        "ethnicity": "BD",
        "language": "bn",
        "bio": "Hi, I am Daniel.",
        "child_condition": "Liver cancer",
        "child_age_of_diagnosis": 15,
        "child_transplant": "Y",
    },
]


class ParentSeeder:
    """Seed parents into the database."""

    PARENT_COUNT = 100

    def __init__(self, faker):
        self.faker = faker
        self.user_seeder = UserSeeder(self.faker)

    def create_parents(self):
        self.generate_parent_fixtures()
        self.generate_random_parents()

    def generate_parent_fixtures(self):
        for data in parent_fixtures:
            self.try_create_parent(data)        

    def generate_random_parents(self):
        parent_count = Parent.objects.count()
        while parent_count < self.PARENT_COUNT:
            print(f"Seeding parent {parent_count}/{self.PARENT_COUNT}", end="\r")
            self.generate_parent()
            parent_count = Parent.objects.count()
        print("Parent seeding complete.      ")

    def generate_parent(self):
        user_data = self.user_seeder.generate_user_data()
        child_condition = self.faker.random_element(elements=(tuple(condition[0] for condition in CONDITION_CHOICES)))
        child_age_of_diagnosis = randint(0, 20)
        child_transplant = self.faker.random_element(elements=(tuple(transplant[0] for transplant in TRANSPLANT_CHOICES)))
        user_data.update({'child_condition': child_condition, 'child_age_of_diagnosis': child_age_of_diagnosis, 'child_transplant': child_transplant})
        self.try_create_parent(user_data)

    def try_create_parent(self, data):
        try:
            self.create_parent(data)
        except:
            pass

    def create_parent(self, data):
        self.user_seeder.create_user(Parent, data)

    