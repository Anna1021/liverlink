from django.core.management.base import BaseCommand

from peer_support.models import User, Parent, Patient, Mentor, Referral, Notification, Message, Conversation, Question, Response
import uuid

from faker import Faker
from random import randint
from peer_support.models.model_choices import *
from peer_support.forms.form_choices import CONDITION_CHOICES, TRANSPLANT_CHOICES

patient_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe', 'date_of_birth': '2000-01-01', 'gender': 'M', 'location': 'GB', 'hospital': 'Croydon Health Services NHS Trust', 'ethnicity': 'BR', 'language': 'en', 'bio': 'Hi, I am John.', 'condition': 'Diabetes', 'age_of_diagnosis': 5},
    {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe', 'date_of_birth': '2008-01-01', 'gender': 'F', 'location': 'FR', 'ethnicity': 'RO', 'language': 'fr', 'bio': 'Hi, I am Jane.', 'condition': 'Hepatitis A', 'age_of_diagnosis': 10, 'transplant': 'Y'},
    {'username': '@charliejohnson', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson', 'date_of_birth': '2006-01-01', 'gender': 'O', 'location': 'BD', 'ethnicity': 'IN', 'language': 'bn', 'bio': 'Hi, I am Charlie.', 'condition': 'Liver cancer', 'age_of_diagnosis': 15},
]

parent_fixtures = [
    {'username': '@jackjones', 'email': 'jack.jones@example.org', 'first_name': 'Jack', 'last_name': 'Jones', 'date_of_birth': '1980-01-01', 'gender': 'M', 'location': 'GB', 'hospital': 'Croydon Health Services NHS Trust', 'ethnicity': 'BR', 'language': 'en', 'bio': 'Hi, I am Jack.', 'child_condition': 'Diabetes', 'child_age_of_diagnosis': 5},
    {'username': '@jilljones', 'email': 'jill.jones@example.org', 'first_name': 'Jill', 'last_name': 'Jones', 'date_of_birth': '1985-04-20', 'gender': 'F', 'location': 'FR', 'ethnicity': 'RO', 'language': 'fr', 'bio': 'Hi, I am Jill.', 'child_condition': 'Hepatitis A', 'child_age_of_diagnosis': 10},
    {'username': '@danielcaesar', 'email': 'daniel.caesar@example.org', 'first_name': 'Daniel', 'last_name': 'Caesar', 'date_of_birth': '1992-03-02', 'gender': 'O', 'location': 'BD', 'ethnicity': 'BD', 'language': 'bn', 'bio': 'Hi, I am Daniel.', 'child_condition': 'Liver cancer', 'child_age_of_diagnosis': 15, 'child_transplant': 'Y'},
]

mentor_fixtures = [
    {'username': '@sarahsmith', 'email': 'sarah.smith@example.org', 'first_name': 'Sarah', 'last_name': 'Smith', 'date_of_birth': '1992-05-15', 'gender': 'F', 'location': 'US', 'hospital': 'Blackpool Teaching Hospitals NHS Foundation Trust', 'ethnicity': 'BR', 'language': 'en', 'bio': 'Hello, I am Sarah.', 'condition': 'Diabetes', 'age_of_diagnosis': 7, 'referral_code':'ABC123'},
    {'username': '@davidbrown', 'email': 'david.brown@example.org', 'first_name': 'David', 'last_name': 'Brown', 'date_of_birth': '1985-09-20', 'gender': 'M', 'location': 'CA', 'hospital': 'Countess of Chester Hospital NHS Foundation Trust', 'ethnicity': 'BR', 'language': 'en', 'bio': 'Hey there, I am David.', 'age_of_diagnosis': 8, 'referral_code':'DEF456'},
    {'username': '@emilywilson', 'email': 'emily.wilson@example.org', 'first_name': 'Emily', 'last_name': 'Wilson', 'date_of_birth': '1978-12-03', 'gender': 'F', 'location': 'AU', 'hospital': 'Blackpool Teaching Hospitals NHS Foundation Trust', 'ethnicity': 'BR', 'language': 'en', 'bio': 'Hi, I am Emily.', 'age_of_diagnosis': 3, 'referral_code':'GHI789'},
]

notification_fixtures = [
    {'title': 'Welcome to Peer Support', 'description': 'Welcome to Peer Support. We are glad to have you here.', 'user':  patient_fixtures[0]},
    {'title': 'New like to your post', 'description': 'Your post has received a new like.', 'user':  patient_fixtures[0]},
    {'title': 'New message', 'description': 'You have received a new message.', 'user': patient_fixtures[0]},
]

message_fixtures = [
    {'sender': patient_fixtures[0], 'content': 'Hello, how are you?'},
    {'sender': parent_fixtures[0], 'content': 'I am good, thank you.'},
    {'sender': parent_fixtures[0], 'content': 'How are you?'},
    {'sender': patient_fixtures[1], 'content': 'I am good'},
    {'sender': parent_fixtures[1], 'content': 'Hi'},
]

conversation_fixtures = [
    {'users': [patient_fixtures[0], parent_fixtures[0]], 'messages': [message_fixtures[0], message_fixtures[1], message_fixtures[2]]},
    {'users': [patient_fixtures[1], parent_fixtures[1]], 'messages': [message_fixtures[3], message_fixtures[4]]},
    {'users': [patient_fixtures[0], parent_fixtures[2]],  'messages': [message_fixtures[1]]},                                
]

question_fixtures = [
    {'author': patient_fixtures[0], 'title': 'Question 1', 'body': 'This is my first question.'},
    {'author': parent_fixtures[0], 'title': 'Question 2', 'body': 'I have a question for you.'},
    {'author': patient_fixtures[1], 'title': 'Question 3', 'body': 'Can you help me with this?'},
    {'author': parent_fixtures[1], 'title': 'Question 4', 'body': 'I need help.'},
]

response_fixtures = [
    {'user': mentor_fixtures[0], 'question': question_fixtures[0], 'body': 'This is my first response.'},
    {'user': mentor_fixtures[1], 'question': question_fixtures[1], 'body': 'I have a response for you.'},
    {'user': mentor_fixtures[2], 'question': question_fixtures[2], 'body': 'I can help you with this.'},
    {'user': parent_fixtures[0], 'question': question_fixtures[3], 'body': 'I can help you.'},
]

class Command(BaseCommand):
    """Build automation command to seed the database."""

    PATIENT_COUNT = 100
    PARENT_COUNT = 100
    MENTOR_COUNT = 100
    NOTIFICATION_COUNT = 500
    MESSAGE_COUNT = 1000
    CONVERSATION_COUNT = 500
    QUESTION_COUNT = 250
    RESPONSE_COUNT = 1000
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

        self.users = User.objects.all()

        self.create_notifications()
        self.notifications = Notification.objects.all()

        self.create_messages()
        self.messages = Message.objects.all()

        # self.create_conversations()
        # self.conversations = Conversation.objects.all()

        self.create_questions()
        self.questions = Question.objects.all()

        self.create_responses()
        self.responses = Response.objects.all()

    def create_patients(self):
        self.generate_patient_fixtures()
        self.generate_random_patients()

    def create_parents(self):
        self.generate_parent_fixtures()
        self.generate_random_parents()

    def create_mentors(self):
        self.generate_mentor_fixtures()
        self.generate_random_mentors()

    def create_notifications(self):
        self.generate_notification_fixtures()
        self.generate_random_notifications()

    def create_messages(self):
        self.generate_message_fixtures()
        self.generate_random_messages()

    # def create_conversations(self):
    #     self.generate_conversation_fixtures()
    #     self.generate_random_conversations()

    def create_questions(self):
        self.generate_question_fixtures()
        self.generate_random_questions()

    def create_responses(self):
        self.generate_response_fixtures()
        self.generate_random_responses()

    def generate_patient_fixtures(self):
        for data in patient_fixtures:
            self.try_create_patient(data)

    def generate_parent_fixtures(self):
        for data in parent_fixtures:
            self.try_create_parent(data)

    def generate_mentor_fixtures(self):
        for data in mentor_fixtures:
            self.try_create_mentor(data)

    def generate_notification_fixtures(self):
        for data in notification_fixtures:
            self.try_create_notification(data)

    def generate_message_fixtures(self):
        for data in message_fixtures:
            self.try_create_message(data)

    # def generate_conversation_fixtures(self):
    #     for data in conversation_fixtures:
    #         self.try_create_conversation(data)

    def generate_question_fixtures(self):
        for data in question_fixtures:
            self.create_question(data)

    def generate_response_fixtures(self):
        for data in response_fixtures:
            self.create_response(data)

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

    def generate_random_notifications(self):
        notification_count = Notification.objects.count()
        while notification_count < self.NOTIFICATION_COUNT:
            print(f"Seeding notification {notification_count}/{self.NOTIFICATION_COUNT}", end='\r')
            self.generate_notification()
            notification_count = Notification.objects.count()
        print("Notification seeding complete.      ")

    def generate_random_messages(self):
        message_count = Message.objects.count()
        while message_count < self.MESSAGE_COUNT:
            print(f"Seeding message {message_count}/{self.MESSAGE_COUNT}", end='\r')
            self.generate_message()
            message_count = Message.objects.count()
        print("Message seeding complete.      ")

    # def generate_random_conversations(self):
    #     conversation_count = Conversation.objects.count()
    #     while conversation_count < self.CONVERSATION_COUNT:
    #         print(f"Seeding conversation {conversation_count}/{self.CONVERSATION_COUNT}", end='\r')
    #         self.generate_conversation()
    #         conversation_count = Conversation.objects.count()
    #     print("Conversation seeding complete.      ")

    def generate_random_questions(self):
        question_count = Question.objects.count()
        while question_count < self.QUESTION_COUNT:
            print(f"Seeding question {question_count}/{self.QUESTION_COUNT}", end='\r')
            self.generate_question()
            question_count = Question.objects.count()
        print("Question seeding complete.      ")

    def generate_random_responses(self):
        response_count = Response.objects.count()
        while response_count < self.RESPONSE_COUNT:
            print(f"Seeding response {response_count}/{self.RESPONSE_COUNT}", end='\r')
            self.generate_response()
            response_count = Response.objects.count()
        print("Response seeding complete.      ")

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
        transplant = self.faker.random_element(elements=(tuple(transplant[0] for transplant in TRANSPLANT_CHOICES)))
        user_data.update({'condition': condition, 'age_of_diagnosis': age_of_diagnosis, 'transplant': transplant})
        self.try_create_patient(user_data)

    def generate_parent(self):
        user_data = self.generate_user_data()
        child_condition = self.faker.random_element(elements=(tuple(condition[0] for condition in CONDITION_CHOICES)))
        child_age_of_diagnosis = randint(0, 20)
        child_transplant = self.faker.random_element(elements=(tuple(transplant[0] for transplant in TRANSPLANT_CHOICES)))
        user_data.update({'child_condition': child_condition, 'child_age_of_diagnosis': child_age_of_diagnosis, 'child_transplant': child_transplant})
        self.try_create_parent(user_data)
    
    def generate_mentor(self):
        user_data = self.generate_user_data()
        condition = self.faker.random_element(elements=(tuple(condition[0] for condition in CONDITION_CHOICES)))
        age_of_diagnosis = randint(0, 30)
        referral_code = uuid.uuid4().hex[:10].upper()
        transplant = self.faker.random_element(elements=(tuple(transplant[0] for transplant in TRANSPLANT_CHOICES)))
        user_data.update({'condition': condition, 'age_of_diagnosis': age_of_diagnosis, 'referral_code': referral_code, 'transplant': transplant})
        self.try_create_mentor(user_data)

    def generate_notification(self):
        title = self.faker.sentence()
        description = self.faker.text(max_nb_chars=100)
        user = self.users[randint(0, len(self.users) - 1)]
        user = {'username': user.username}
        self.try_create_notification({'title': title, 'description': description, 'user': user})

    def generate_message(self):
        sender = self.users[randint(0, len(self.users) - 1)]
        content = self.faker.text(max_nb_chars=100)
        self.try_create_message({'sender': sender, 'content': content})

    # def generate_conversation(self):
    #     users = [self.users[randint(0, len(self.users) - 1)], self.users[randint(0, len(self.users) - 1)]]
    #     messages = [self.messages[randint(0, len(self.messages) - 1)], self.messages[randint(0, len(self.messages) - 1)]]
    #     users = {'usernames': [user.username for user in users]}
    #     self.try_create_conversation({'users': users, 'messages': messages})

    def generate_question(self):
        author = self.users[randint(0, len(self.users) - 1)]
        title = self.faker.sentence()
        body = self.faker.text(max_nb_chars=100)
        author = {'username': author.username}
        self.try_create_question({'author': author, 'title': title, 'body': body})

    def generate_response(self):
        user = self.users[randint(0, len(self.users) - 1)]
        question = self.questions[randint(0, len(self.questions) - 1)]
        body = self.faker.text(max_nb_chars=100)
        user = {'username': user.username}
        question = {'title': question.title} # Can we create a primary key for response model? such as id 
        self.try_create_response({'user': user, 'question': question, 'body': body})
        
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

    def try_create_notification(self, data):
        try:
            self.create_notification(data)
        except:
            pass

    def try_create_message(self, data):
        try:
            self.create_message(data)
        except:
            pass

    # def try_create_conversation(self, data):
    #     # try:
    #     self.create_conversation(data)
    #     # except:
    #     #     pass

    def try_create_question(self, data):
        try:
            self.create_question(data)
        except:
            pass

    def try_create_response(self, data):
        try:
            self.create_response(data)
        except:
            pass

    def create_user(self, model, data):
        user = model.objects.create(**data)
        user.set_password(Command.DEFAULT_PASSWORD)
        if data['username'] == '@johndoe':
            user.is_superuser = True
            user.is_staff = True
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

    def create_notification(self, data):
        data['user'] = self.get_user(data['user'])
        Notification.objects.create(**data)

    def create_message(self, data):
        message = Message.objects.create(**data)
        message.save()

    # def create_conversation(self, data):
    #     data['users'] = [self.get_user(user) for user in data['users']]
    #     Conversation.objects.create()

    def create_question(self, data):
        data['author'] = self.get_user(data['author'])
        Question.objects.create(**data)

    def create_response(self, data):
        data['user'] = self.get_user(data['user'])
        data['question'] = Question.objects.filter(title=data['question']['title']).first() # Change this when primary key implemented
        # Change it to a get
        Response.objects.create(**data)

    def get_user(self, data):
        return User.objects.get(username=data['username'])

def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
    return first_name + '.' + last_name + '@example.org'