from django.core.management.base import BaseCommand, CommandError

from peer_support.models import User, Parent, Patient

import pytz
from faker import Faker
from random import randint, random

patient_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe', 'date_of_birth': '2000-01-01', 'gender': 'M', 'location': 'GB', 'ethnicity': 'BR', 'language': 'en', 'bio': 'Hi, I am John.', 'condition': 'Diabetes', 'age_of_diagnosis': 5},
    {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe', 'date_of_birth': '2008-01-01', 'gender': 'F', 'location': 'FR', 'ethnicity': 'RO', 'language': 'fr', 'bio': 'Hi, I am Jane.', 'condition': 'Hepatitis A', 'age_of_diagnosis': 10},
    {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson', 'date_of_birth': '2006-01-01', 'gender': 'O', 'location': 'BD', 'ethnicity': 'IN', 'language': 'bn', 'bio': 'Hi, I am Charlie.', 'condition': 'Liver cancer', 'age_of_diagnosis': 15},
]

parent_fixtures = [
    {'username': '@jackjones', 'email': 'jack.jones@example.org', 'first_name': 'Jack', 'last_name': 'Jones', 'date_of_birth': '1980-01-01', 'gender': 'M', 'location': 'GB', 'ethnicity': 'BR', 'language': 'en', 'bio': 'Hi, I am Jack.', 'child_condition': 'Diabetes', 'child_age_of_diagnosis': 5},
    {'username': '@jilljones', 'email': 'jill.jones@example.org', 'first_name': 'Jill', 'last_name': 'Jones', 'date_of_birth': '1985-04-20', 'gender': 'F', 'location': 'FR', 'ethnicity': 'RO', 'language': 'fr', 'bio': 'Hi, I am Jill.', 'child_condition': 'Hepatitis A', 'child_age_of_diagnosis': 10},
    {'username': '@jamescaesar', 'email': 'james.caesar@example.org', 'first_name': 'James', 'last_name': 'Caesar', 'date_of_birth': '1992-03-02', 'gender': 'O', 'location': 'BD', 'ethnicity': 'BD', 'language': 'bn', 'bio': 'Hi, I am James.', 'child_condition': 'Liver cancer', 'child_age_of_diagnosis': 15},
]

class Command(BaseCommand):
    """Build automation command to seed the database."""

    PATIENT_COUNT = 100
    PARENT_COUNT = 100
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    def __init__(self):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_patients()
        self.patients = Patient.objects.all()

        self.create_parents()
        self.parents = Parent.objects.all()

    def create_patients(self):
        self.generate_patient_fixtures()
        self.generate_random_patients()

    def create_parents(self):
        self.generate_parent_fixtures()
        self.generate_random_parents()

    def generate_patient_fixtures(self):
        for data in patient_fixtures:
            self.try_create_patient(data)

    def generate_parent_fixtures(self):
        for data in parent_fixtures:
            self.try_create_parent(data)

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

    def generate_patient(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        date_of_birth = self.faker.date_of_birth(minimum_age=16, maximum_age=100)
        gender = self.faker.random_element(elements=('M', 'F', 'O', 'N'))
        location = self.faker.country()
        ethnicity = self.faker.random_element(elements=('White', 'Black', 'Asian', 'Mixed', 'Other'))
        language = self.faker.language_code()
        bio = self.faker.text(max_nb_chars=100)
        condition = self.faker.random_element(elements=('Diabetes', 'Hepatitis A', 'Liver cancer', 'Cysts', 'Other'))
        age_of_diagnosis = randint(0, 20)
        self.try_create_patient({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name, 'date_of_birth': date_of_birth, 'gender': gender, 'location': location, 'ethnicity': ethnicity, 'language': language, 'bio': bio, 'condition': condition, 'age_of_diagnosis': age_of_diagnosis})

    def generate_parent(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        date_of_birth = self.faker.date_of_birth(minimum_age=16, maximum_age=100)
        gender = self.faker.random_element(elements=('M', 'F', 'O', 'N'))
        location = self.faker.country()
        ethnicity = self.faker.random_element(elements=('White', 'Black', 'Asian', 'Mixed', 'Other'))
        language = self.faker.language_code()
        bio = self.faker.text(max_nb_chars=100)
        child_condition = self.faker.random_element(elements=('Diabetes', 'Hepatitis A', 'Liver cancer', 'Cysts', 'Other'))
        child_age_of_diagnosis = randint(0, 30)
        self.create_parent({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name, 'date_of_birth': date_of_birth, 'gender': gender, 'location': location, 'ethnicity': ethnicity, 'language': language, 'bio': bio, 'child_condition': child_condition, 'child_age_of_diagnosis': child_age_of_diagnosis})

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

    def create_patient(self, data):
        Patient.objects.create(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=data['date_of_birth'],
            gender=data['gender'],
            location=data['location'],
            ethnicity=data['ethnicity'],
            language=data['language'],
            bio=data['bio'],
            condition=self.faker.random_element(elements=('Diabetes', 'Hepatitis A', 'Liver cancer', 'Cysts', 'Other')),
            age_of_diagnosis=randint(0, 30),
        )

    def create_parent(self, data):
        Parent.objects.create(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=data['date_of_birth'],
            gender=data['gender'],
            location=data['location'],
            ethnicity=data['ethnicity'],
            language=data['language'],
            bio=data['bio'],
            child_condition=self.faker.random_element(elements=('Diabetes', 'Hepatitis A', 'Liver cancer', 'Cysts', 'Other')),
            child_age_of_diagnosis=randint(0, 30),
        )

def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
    return first_name + '.' + last_name + '@example.org'