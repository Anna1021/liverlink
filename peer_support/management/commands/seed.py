from django.core.management.base import BaseCommand

from peer_support.models import Parent, Patient, Mentor, Referral
import uuid

from faker import Faker
from random import randint
from peer_support.models.model_choices import *
from peer_support.forms.form_choices import CONDITION_CHOICES

patient_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe', 'date_of_birth': '2000-01-01', 'gender': 'M', 'location': 'GB', 'hospital': 'Croydon Health Services NHS Trust', 'ethnicity': 'BR', 'language': 'en', 'bio': 'Hi, I am John.', 'condition': 'Diabetes', 'age_of_diagnosis': 5},
    {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe', 'date_of_birth': '2008-01-01', 'gender': 'F', 'location': 'FR', 'ethnicity': 'RO', 'language': 'fr', 'bio': 'Hi, I am Jane.', 'condition': 'Hepatitis A', 'age_of_diagnosis': 10},
    {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson', 'date_of_birth': '2006-01-01', 'gender': 'O', 'location': 'BD', 'ethnicity': 'IN', 'language': 'bn', 'bio': 'Hi, I am Charlie.', 'condition': 'Liver cancer', 'age_of_diagnosis': 15},
]

parent_fixtures = [
    {'username': '@jackjones', 'email': 'jack.jones@example.org', 'first_name': 'Jack', 'last_name': 'Jones', 'date_of_birth': '1980-01-01', 'gender': 'M', 'location': 'GB', 'hospital': 'Croydon Health Services NHS Trust', 'ethnicity': 'BR', 'language': 'en', 'bio': 'Hi, I am Jack.', 'child_condition': 'Diabetes', 'child_age_of_diagnosis': 5},
    {'username': '@jilljones', 'email': 'jill.jones@example.org', 'first_name': 'Jill', 'last_name': 'Jones', 'date_of_birth': '1985-04-20', 'gender': 'F', 'location': 'FR', 'ethnicity': 'RO', 'language': 'fr', 'bio': 'Hi, I am Jill.', 'child_condition': 'Hepatitis A', 'child_age_of_diagnosis': 10},
    {'username': '@danielcaesar', 'email': 'daniel.caesar@example.org', 'first_name': 'Daniel', 'last_name': 'Caesar', 'date_of_birth': '1992-03-02', 'gender': 'O', 'location': 'BD', 'ethnicity': 'BD', 'language': 'bn', 'bio': 'Hi, I am Daniel.', 'child_condition': 'Liver cancer', 'child_age_of_diagnosis': 15},
]

mentor_fixtures = [
    {'username': '@sarahsmith', 'email': 'sarah.smith@example.org', 'first_name': 'Sarah', 'last_name': 'Smith', 'date_of_birth': '1992-05-15', 'gender': 'F', 'location': 'US', 'hospital': 'Blackpool Teaching Hospitals NHS Foundation Trust', 'ethnicity': 'BR', 'language': 'en', 'bio': 'Hello, I am Sarah.', 'condition': 'Diabetes', 'age_of_diagnosis': 7, 'referral_code':'ABC123'},
    {'username': '@davidbrown', 'email': 'david.brown@example.org', 'first_name': 'David', 'last_name': 'Brown', 'date_of_birth': '1985-09-20', 'gender': 'M', 'location': 'CA', 'hospital': 'Countess of Chester Hospital NHS Foundation Trust', 'ethnicity': 'BR', 'language': 'en', 'bio': 'Hey there, I am David.', 'age_of_diagnosis': 8, 'referral_code':'DEF456'},
    {'username': '@emilywilson', 'email': 'emily.wilson@example.org', 'first_name': 'Emily', 'last_name': 'Wilson', 'date_of_birth': '1978-12-03', 'gender': 'F', 'location': 'AU', 'hospital': 'Blackpool Teaching Hospitals NHS Foundation Trust', 'ethnicity': 'BR', 'language': 'en', 'bio': 'Hi, I am Emily.', 'age_of_diagnosis': 3, 'referral_code':'GHI789'},
]

class Command(BaseCommand):
    """Build automation command to seed the database."""

    PATIENT_COUNT = 100
    PARENT_COUNT = 100
    MENTOR_COUNT = 100
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    def __init__(self):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_patients()
        self.patients = Patient.objects.all()

        self.create_parents()
        self.parents = Parent.objects.all()

        self.create_mentors()
        self.mentors = Mentor.objects.all()

    def create_patients(self):
        self.generate_patient_fixtures()
        self.generate_random_patients()

    def create_parents(self):
        self.generate_parent_fixtures()
        self.generate_random_parents()

    def create_mentors(self):
        self.generate_mentor_fixtures()
        self.generate_random_mentors()

    def generate_patient_fixtures(self):
        for data in patient_fixtures:
            self.try_create_patient(data)

    def generate_parent_fixtures(self):
        for data in parent_fixtures:
            self.try_create_parent(data)

    def generate_mentor_fixtures(self):
        for data in mentor_fixtures:
            self.try_create_mentor(data)

    def generate_random_patients(self):
        patient_count = Patient.objects.count()
        while patient_count < self.PATIENT_COUNT:
            print(f"Seeding patient {patient_count}/{self.PATIENT_COUNT}", end='\r')
            self.generate_patient()
            patient_count = Patient.objects.count()
        print("Patient seeding complete.      ")

    def generate_random_parents(self):
        parent_count = Parent.objects.count()
        while parent_count < self.PARENT_COUNT:
            print(f"Seeding parent {parent_count}/{self.PARENT_COUNT}", end='\r')
            self.generate_parent()
            parent_count = Parent.objects.count()
        print("Parent seeding complete.      ")

    def generate_random_mentors(self):
        mentor_count = Mentor.objects.count()
        while mentor_count < self.MENTOR_COUNT:
            print(f"Seeding mentor {mentor_count}/{self.MENTOR_COUNT}", end='\r')
            self.generate_mentor()
            mentor_count = Mentor.objects.count()
        print("Mentor seeding complete.      ")

    def generate_user_data(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        date_of_birth = self.faker.date_of_birth(minimum_age=16, maximum_age=100)
        gender = self.faker.random_element(elements=(tuple(gender[0] for gender in GENDER_CHOICES)))
        location = self.faker.random_element(elements=(tuple(country[0] for country in COUNTRY_CHOICES)))
        hospital = self.faker.random_element(elements=(tuple(hospital[0] for hospital in HOSPITAL_CHOICES)))
        ethnicity = self.faker.random_element(elements=[ethnicity[0] for group in ETHNICITY_CHOICES for ethnicity in group[1]])
        language = self.faker.random_element(elements=(tuple(language[0] for language in LANGUAGE_CHOICES)))
        bio = self.faker.text(max_nb_chars=100)
        return {'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name, 'date_of_birth': date_of_birth, 'gender': gender, 'location': location, 'hospital': hospital, 'ethnicity': ethnicity, 'language': language, 'bio': bio}

    def generate_patient(self):
        user_data = self.generate_user_data()
        condition = self.faker.random_element(elements=(tuple(condition[0] for condition in CONDITION_CHOICES)))
        age_of_diagnosis = randint(0, 20)
        user_data.update({'condition': condition, 'age_of_diagnosis': age_of_diagnosis})
        self.try_create_patient(user_data)

    def generate_parent(self):
        user_data = self.generate_user_data()
        child_condition = self.faker.random_element(elements=(tuple(condition[0] for condition in CONDITION_CHOICES)))
        child_age_of_diagnosis = randint(0, 30)
        user_data.update({'child_condition': child_condition, 'child_age_of_diagnosis': child_age_of_diagnosis})
        self.try_create_parent(user_data)
    
    def generate_mentor(self):
        user_data = self.generate_user_data()
        condition = self.faker.random_element(elements=(tuple(condition[0] for condition in CONDITION_CHOICES)))
        age_of_diagnosis = randint(0, 30)
        user_data.update({'condition': condition, 'age_of_diagnosis': age_of_diagnosis})
        referral_code = uuid.uuid4().hex[:10].upper()
        user_data.update({'referral_code': referral_code})
        self.try_create_mentor(user_data)
        
    def try_create_patient(self, data):
        try:
            self.create_patient(data)
        except:
            pass

    def try_create_parent(self, data):
        try:
            self.create_parent(data)
        except:
            pass
    
    def try_create_mentor(self, data):
        try:
            self.create_mentor(data)
        except:
            pass

    def create_user(self, model, data):
        user = model.objects.create(**data)
        user.set_password(Command.DEFAULT_PASSWORD)
        user.save()
        if model == Mentor:
            Referral.objects.create(referrer=user, code=data['referral_code'])
        return user

    def create_patient(self, data):
        self.create_user(Patient, data)

    def create_parent(self, data):
        self.create_user(Parent, data)

    def create_mentor(self, data):
        self.create_user(Mentor, data)

def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
    return first_name + '.' + last_name + '@example.org'