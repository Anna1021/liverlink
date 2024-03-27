from random import randint
from peer_support.forms.form_choices import CONDITION_CHOICES, TRANSPLANT_CHOICES
from peer_support.management.commands.seeders.user_seeder import UserSeeder
from peer_support.models import Patient

patient_fixtures = [
    {
        "username": "@johndoe",
        "email": "john.doe@example.org",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "2000-01-01",
        "gender": "M",
        "location": "GB",
        "hospital": "Croydon Health Services NHS Trust",
        "ethnicity": "BR",
        "language": "en",
        "bio": "Hi, I am John.",
        "condition": "Diabetes",
        "age_of_diagnosis": 5,
    },
    {
        "username": "@janedoe",
        "email": "jane.doe@example.org",
        "first_name": "Jane",
        "last_name": "Doe",
        "date_of_birth": "2008-01-01",
        "gender": "F",
        "location": "FR",
        "ethnicity": "RO",
        "language": "fr",
        "bio": "Hi, I am Jane.",
        "condition": "Hepatitis A",
        "age_of_diagnosis": 10,
        "transplant": "Y",
    },
    {
        "username": "@charliejohnson",
        "email": "charlie.johnson@example.org",
        "first_name": "Charlie",
        "last_name": "Johnson",
        "date_of_birth": "2006-01-01",
        "gender": "O",
        "location": "BD",
        "ethnicity": "IN",
        "language": "bn",
        "bio": "Hi, I am Charlie.",
        "condition": "Liver cancer",
        "age_of_diagnosis": 15,
    },
]


class PatientSeeder:
    """Seed patients into the database."""

    PATIENT_COUNT = 100
    
    def __init__(self, faker):
        self.faker = faker
        self.user_seeder = UserSeeder(self.faker)

    def create_patients(self):
        self.generate_patient_fixtures()
        self.generate_random_patients()

    def generate_patient_fixtures(self):
        for data in patient_fixtures:
            self.try_create_patient(data)

    def generate_random_patients(self):
        patient_count = Patient.objects.count()
        while patient_count < self.PATIENT_COUNT:
            print(f"Seeding patient {patient_count}/{self.PATIENT_COUNT}", end="\r")
            self.generate_patient()
            patient_count = Patient.objects.count()
        print("Patient seeding complete.      ")

    def generate_patient(self):
        user_data = self.user_seeder.generate_user_data()
        date_of_birth = self.faker.date_of_birth(minimum_age=16, maximum_age=25)
        condition = self.faker.random_element(elements=(tuple(condition[0] for condition in CONDITION_CHOICES)))
        age_of_diagnosis = randint(0, 20)
        transplant = self.faker.random_element(elements=(tuple(transplant[0] for transplant in TRANSPLANT_CHOICES)))
        user_data.update({'date_of_birth': date_of_birth, 'condition': condition, 'age_of_diagnosis': age_of_diagnosis, 'transplant': transplant})
        self.try_create_patient(user_data)

    def try_create_patient(self, data):
        try:
            self.create_patient(data)
        except:
            pass

    def create_patient(self, data):
        self.user_seeder.create_user(Patient, data)