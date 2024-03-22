from django.core.management.base import BaseCommand
from peer_support.models import *
import uuid
from faker import Faker
from random import randint
import random
from django.contrib.contenttypes.models import ContentType
from peer_support.models.model_choices import *
from peer_support.forms.form_choices import CONDITION_CHOICES, TRANSPLANT_CHOICES

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

mentor_fixtures = [
    {
        "username": "@sarahsmith",
        "email": "sarah.smith@example.org",
        "first_name": "Sarah",
        "last_name": "Smith",
        "date_of_birth": "1992-05-15",
        "gender": "F",
        "location": "US",
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
        "location": "CA",
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
        "hospital": "Blackpool Teaching Hospitals NHS Foundation Trust",
        "ethnicity": "BR",
        "language": "en",
        "bio": "Hi, I am Emily.",
        "age_of_diagnosis": 3,
        "referral_code": "GHI789",
    },
]

friend_request_fixtures = [
    {"sender": patient_fixtures[0], "receiver": parent_fixtures[0]},
    {"sender": parent_fixtures[0], "receiver": patient_fixtures[0]},
    {"sender": patient_fixtures[1], "receiver": parent_fixtures[1]},
]

message_fixtures = [
    {"sender": patient_fixtures[0], "content": "Hello, how are you?"},
    {"sender": parent_fixtures[0], "content": "I am good, thank you."},
    {"sender": parent_fixtures[0], "content": "How are you?"},
    {"sender": patient_fixtures[1], "content": "I am good"},
    {"sender": parent_fixtures[1], "content": "Hi"},
]

conversation_fixtures = [
    {
        "users": [patient_fixtures[0], parent_fixtures[0]],
        "messages": [message_fixtures[0], message_fixtures[1], message_fixtures[2]],
    },
    {
        "users": [patient_fixtures[1], parent_fixtures[1]],
        "messages": [message_fixtures[3], message_fixtures[4]],
    },
    {
        "users": [patient_fixtures[0], parent_fixtures[2]],
        "messages": [message_fixtures[1]],
    },
]

notification_fixtures = [
    {
        "title": "Welcome to Peer Support",
        "description": "Welcome to Peer Support. We are glad to have you here.",
        "user": patient_fixtures[0],
    },
    {
        "title": "New Friend Request",
        "description": "@jackjones has sent you a friend request.",
        "user": patient_fixtures[0],
        "notifying_user": parent_fixtures[0],
        "content_type": ContentType.objects.get_for_model(FriendRequest),
        "object_id": 1
    },
    {
        "title": "New Conversation",
        "description": "@jackjones has added you to a conversation.",
        "user": patient_fixtures[0],
        "notifying_user": parent_fixtures[0],
        "content_type": ContentType.objects.get_for_model(Conversation),
        "object_id": 1
    },
]

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
    {"author": parent_fixtures[1], "title": "Question 4", "body": "I need help."},
]

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

report_fixtures = [
    {
        "reporter": patient_fixtures[0],
        "reason": "abuse",
        "content_type": "User",
        "object_id": patient_fixtures[1],
    },
    {
        "reporter": parent_fixtures[0],
        "reason": "other",
        "content_type": "Message",
        "object_id": message_fixtures[0],
    },
    {
        "reporter": patient_fixtures[2],
        "reason": "spam",
        "content_type": "User",
        "object_id": parent_fixtures[0],
    },
]

post_fixtures = [
    {"author": patient_fixtures[0], "content": "This is my post"},
    {"author": parent_fixtures[0], "content": "Hello world!", "visibility": "F"},
    {"author": mentor_fixtures[0], "content": "Hello, I am a mentor."},
]

post_comment_fixtures = [
    {
        "post": post_fixtures[0],
        "author": parent_fixtures[0],
        "content": "This is my comment.",
    },
    {"post": post_fixtures[1], "author": patient_fixtures[0], "content": "Hello!"},
    {
        "post": post_fixtures[2],
        "author": mentor_fixtures[0],
        "content": "Hi, I am a mentor.",
    },
]

feedback_fixtures = [
    {"title": "Fix this", "content": "This is broken."},
    {"title": "Improve that", "content": "This could be improved"},
    {"title": "Add this", "content": "This is missing."},
]


class Command(BaseCommand):
    """Build automation command to seed the database."""

    PATIENT_COUNT = 100
    PARENT_COUNT = 100
    MENTOR_COUNT = 100
    FRIEND_REQUEST_COUNT = 100
    NOTIFICATION_COUNT = 500
    CONVERSATION_COUNT = 500
    QUESTION_COUNT = 250
    RESPONSE_COUNT = 1000
    REPORT_COUNT = 250
    POST_COUNT = 500
    POST_COMMENT_COUNT = 1000
    FEEDBACK_COUNT = 500
    DEFAULT_PASSWORD = "Password123"
    help = "Seeds the database with sample data"

    def __init__(self):
        self.faker = Faker("en_GB")

    def handle(self, *args, **options):
        self.create_patients()
        self.patients = Patient.objects.all()

        self.create_parents()
        self.parents = Parent.objects.all()

        self.create_mentors()
        self.mentors = Mentor.objects.all()

        self.users = User.objects.all()

        self.seed_friends()

        self.seed_blocked_users()

        self.create_friend_requests()
        self.friend_requests = FriendRequest.objects.all()

        self.create_messages()
        self.messages = Message.objects.all()

        self.create_conversations()
        self.conversations = Conversation.objects.all()

        self.create_questions()
        self.questions = Question.objects.all()

        self.create_responses()
        self.responses = Response.objects.all()

        self.create_reports()
        self.reports = Report.objects.all()

        self.create_posts()
        self.posts = Post.objects.all()

        self.create_post_comments()
        self.post_comments = PostComment.objects.all()

        self.create_feedbacks()
        self.feedback = Feedback.objects.all()

        self.create_notifications()
        self.notifications = Notification.objects.all()

    def create_patients(self):
        self.generate_patient_fixtures()
        self.generate_random_patients()

    def create_parents(self):
        self.generate_parent_fixtures()
        self.generate_random_parents()

    def create_mentors(self):
        self.generate_mentor_fixtures()
        self.generate_random_mentors()

    def create_friend_requests(self):
        self.generate_friend_request_fixtures()
        self.generate_random_friend_requests()

    def create_notifications(self):
        self.generate_notification_fixtures()
        self.generate_random_notifications()

    def create_messages(self):
        self.generate_message_fixtures()

    def create_conversations(self):
        self.generate_conversation_fixtures()
        self.generate_random_conversations()

    def create_questions(self):
        self.generate_question_fixtures()
        self.generate_random_questions()

    def create_responses(self):
        self.generate_response_fixtures()
        self.generate_random_responses()

    def create_reports(self):
        self.generate_report_fixtures()
        self.generate_random_reports()

    def create_posts(self):
        self.generate_post_fixtures()
        self.generate_random_posts()

    def create_post_comments(self):
        self.generate_post_comment_fixtures()
        self.generate_random_post_comments()

    def create_feedbacks(self):
        self.generate_feedback_fixtures()
        self.generate_random_feedbacks()

    def generate_patient_fixtures(self):
        for data in patient_fixtures:
            self.try_create_patient(data)

    def generate_parent_fixtures(self):
        for data in parent_fixtures:
            self.try_create_parent(data)

    def generate_mentor_fixtures(self):
        for data in mentor_fixtures:
            self.try_create_mentor(data)

    def generate_friend_request_fixtures(self):
        for data in friend_request_fixtures:
            self.try_create_friend_request(data)

    def generate_notification_fixtures(self):
        for data in notification_fixtures:
            self.try_create_notification(data)

    def generate_message_fixtures(self):
        for data in message_fixtures:
            self.try_create_message(data)

    def generate_conversation_fixtures(self):
        for data in conversation_fixtures:
            self.try_create_conversation(data)

    def generate_question_fixtures(self):
        for data in question_fixtures:
            self.create_question(data)

    def generate_response_fixtures(self):
        for data in response_fixtures:
            self.create_response(data)

    def generate_report_fixtures(self):
        for data in report_fixtures:
            self.create_report(data)

    def generate_post_fixtures(self):
        for data in post_fixtures:
            self.create_post(data)

    def generate_post_comment_fixtures(self):
        for data in post_comment_fixtures:
            self.create_post_comment(data)

    def generate_feedback_fixtures(self):
        for data in feedback_fixtures:
            self.create_feedback(data)

    def generate_random_patients(self):
        patient_count = Patient.objects.count()
        while patient_count < self.PATIENT_COUNT:
            print(f"Seeding patient {patient_count}/{self.PATIENT_COUNT}", end="\r")
            self.generate_patient()
            patient_count = Patient.objects.count()
        print("Patient seeding complete.      ")

    def generate_random_parents(self):
        parent_count = Parent.objects.count()
        while parent_count < self.PARENT_COUNT:
            print(f"Seeding parent {parent_count}/{self.PARENT_COUNT}", end="\r")
            self.generate_parent()
            parent_count = Parent.objects.count()
        print("Parent seeding complete.      ")

    def generate_random_mentors(self):
        mentor_count = Mentor.objects.count()
        while mentor_count < self.MENTOR_COUNT:
            print(f"Seeding mentor {mentor_count}/{self.MENTOR_COUNT}", end="\r")
            self.generate_mentor()
            mentor_count = Mentor.objects.count()
        print("Mentor seeding complete.      ")

    def generate_random_friend_requests(self):
        friend_request_count = FriendRequest.objects.count()
        while friend_request_count < self.FRIEND_REQUEST_COUNT:
            print(f"Seeding friend request {friend_request_count}/{self.FRIEND_REQUEST_COUNT}", end='\r')
            self.generate_friend_request()
            friend_request_count = FriendRequest.objects.count()
        print("Friend request seeding complete.      ")

    def generate_random_notifications(self):
        notification_count = Notification.objects.count()
        while notification_count < self.NOTIFICATION_COUNT:
            print(f"Seeding notification {notification_count}/{self.NOTIFICATION_COUNT}", end='\r')
            self.generate_notification()
            notification_count = Notification.objects.count()
        print("Notification seeding complete.      ")

    def generate_random_conversations(self):
        conversation_count = Conversation.objects.count()
        while conversation_count < self.CONVERSATION_COUNT:
            print(f"Seeding conversation {conversation_count}/{self.CONVERSATION_COUNT}", end='\r')
            self.generate_conversation()
            conversation_count = Conversation.objects.count()
        print("Conversation seeding complete.      ")

    def generate_random_questions(self):
        question_count = Question.objects.count()
        while question_count < self.QUESTION_COUNT:
            print(f"Seeding question {question_count}/{self.QUESTION_COUNT}", end="\r")
            self.generate_question()
            question_count = Question.objects.count()
        print("Question seeding complete.      ")

    def generate_random_responses(self):
        response_count = Response.objects.count()
        while response_count < self.RESPONSE_COUNT:
            print(f"Seeding response {response_count}/{self.RESPONSE_COUNT}", end="\r")
            self.generate_response()
            response_count = Response.objects.count()
        print("Response seeding complete.      ")

    def generate_random_reports(self):
        report_count = Report.objects.count()
        while report_count < self.REPORT_COUNT:
            print(f"Seeding report {report_count}/{self.REPORT_COUNT}", end="\r")
            self.generate_report()
            report_count = Report.objects.count()
        print("Report seeding complete.      ")

    def generate_random_posts(self):
        post_count = Post.objects.count()
        while post_count < self.POST_COUNT:
            print(f"Seeding post {post_count}/{self.POST_COUNT}", end="\r")
            self.generate_post()
            post_count = Post.objects.count()
        print("Post seeding complete.      ")

    def generate_random_post_comments(self):
        post_comment_count = PostComment.objects.count()
        while post_comment_count < self.POST_COMMENT_COUNT:
            print(f"Seeding post comment {post_comment_count}/{self.POST_COMMENT_COUNT}", end='\r')
            self.generate_post_comment()
            post_comment_count = PostComment.objects.count()
        print("Post comment seeding complete.      ")

    def generate_random_feedbacks(self):
        feedback_count = Feedback.objects.count()
        while feedback_count < self.FEEDBACK_COUNT:
            print(f"Seeding feedback {feedback_count}/{self.FEEDBACK_COUNT}", end="\r")
            self.generate_feedback()
            feedback_count = Feedback.objects.count()
        print("Feedback seeding complete.      ")

    def generate_user_data(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        date_of_birth = self.faker.date_of_birth(minimum_age=16, maximum_age=100)
        gender = self.faker.random_element(elements=(tuple(gender[0] for gender in GENDER_CHOICES)))
        location = self.faker.random_element(elements=(tuple(country[0] for country in COUNTRY_CHOICES)))
        hospital = ""
        if location == 'GB':
            hospital = self.faker.random_element(elements=(tuple(hospital[0] for hospital in HOSPITAL_CHOICES)))
        ethnicity = self.faker.random_element(elements=[ethnicity[0] for group in ETHNICITY_CHOICES for ethnicity in group[1]])
        language = self.faker.random_element(elements=(tuple(language[0] for language in LANGUAGE_CHOICES)))
        bio = self.faker.text(max_nb_chars=100)
        profile_picture = self.faker.random_element(elements=(tuple(profile_picture for profile_picture in PROFILE_PICTURE_CHOICES)))
        return {'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name, 'date_of_birth': date_of_birth, 'gender': gender, 'location': location, 'hospital': hospital, 'ethnicity': ethnicity, 'language': language, 'bio': bio, 'profile_picture': profile_picture}

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

    def seed_friends(self):
        print("Seeding friends...", end='\r')
        for user in self.users:
            friends_count = user.friends.count()
            if friends_count >= 10:
                continue
            for _ in range(randint(1, 10 - friends_count)):
                friend = self.users[randint(0, len(self.users) - 1)]
                if friend != user and friend not in user.friends.all():
                    user.friends.add(friend)

    def seed_blocked_users(self):
        print("Seeding blocked users...", end='\r')
        for user in self.users:
            blocked_user_count = user.blocked_users.count()
            if blocked_user_count >= 10:
                continue
            for _ in range(randint(1, 10 - blocked_user_count)):
                blocked_user = self.users[randint(0, len(self.users) - 1)]
                if blocked_user != user and blocked_user not in user.friends.all() and blocked_user not in user.blocked_users.all():
                    user.blocked_users.add(blocked_user)

    def generate_friend_request(self):
        sender = self.users[randint(0, len(self.users) - 1)]
        receiver = self.users[randint(0, len(self.users) - 1)]
        sender = {"username": sender.username}
        receiver = {"username": receiver.username}
        self.try_create_friend_request({"sender": sender, "receiver": receiver})

    def generate_notification(self):
        user = self.users[randint(0, len(self.users) - 1)]
        title = None
        description = None
        notifying_user = None
        content_type = None
        object_id = None
        if self.friend_requests.filter(receiver=user) and random.choice([True, False]):
            friend_request = random.choice(self.friend_requests.filter(receiver=user))
            notifying_user = friend_request.sender
            content_type = ContentType.objects.get_for_model(FriendRequest)
            object_id = friend_request.id
        elif self.post_comments.filter(post__author=user) and random.choice([True, False]):
            post_comment = random.choice(self.post_comments.filter(post__author=user))
            notifying_user = post_comment.author
            content_type = ContentType.objects.get_for_model(PostComment)
            object_id = post_comment.id
        else:
            title = self.faker.sentence()
            description = self.faker.text(max_nb_chars=100)
        user = {"username": user.username}
        self.try_create_notification({"title": title, "description": description, "user": user, "notifying_user": notifying_user,
                                      "content_type": content_type, "object_id": object_id})

    def generate_conversation(self):
        users = [
            self.users[randint(0, len(self.users) - 1)],
            self.users[randint(0, len(self.users) - 1)],
        ]
        users = {"usernames": [user.username for user in users]}
        messages = []
        for _ in range(randint(1, 15)):
            sender = users["usernames"][randint(0, len(users["usernames"]) - 1)]
            content = self.faker.text(max_nb_chars=100)
            message = {"sender": sender, "content": content}
            messages.append(message)
        self.try_create_conversation({"users": users, "messages": messages})

    def generate_question(self):
        author = self.users[randint(0, len(self.users) - 1)]
        title = self.faker.sentence()
        body = self.faker.text(max_nb_chars=100)
        author = {"username": author.username}
        self.try_create_question({"author": author, "title": title, "body": body})

    def generate_response(self):
        user = self.users[randint(0, len(self.users) - 1)]
        question = self.questions[randint(0, len(self.questions) - 1)]
        body = self.faker.text(max_nb_chars=100)
        user = {"username": user.username}
        question = {"title": question.title}
        self.try_create_response({"user": user, "question": question, "body": body})

    def generate_report(self):
        reporter = self.users[randint(0, len(self.users) - 1)]
        reason = self.faker.random_element(elements=(tuple(report[0] for report in REPORT_CHOICES)))
        content_type = self.faker.random_element(elements=("user", "message"))
        object_id = (self.get_content_type(content_type)
            .model_class()
            .objects.order_by("?")
            .first()
            .pk
        )
        reporter = {"username": reporter.username}
        self.try_create_report({"reporter": reporter, "reason": reason,  "content_type": content_type, "object_id": object_id})

    def generate_post(self):
        author = self.users[randint(0, len(self.users) - 1)]
        content = self.faker.text(max_nb_chars=280)
        visibility = self.faker.random_element(elements=("G", "F"))
        author = {"username": author.username}
        self.try_create_post({"author": author, "content": content, "visibility": visibility})

    def generate_post_comment(self):
        post = self.posts[randint(0, len(self.posts) - 1)]
        author = self.users[randint(0, len(self.users) - 1)]
        content = self.faker.text(max_nb_chars=255)
        post = {"content": post.content}
        author = {"username": author.username}
        self.try_create_post_comment(
            {"post": post, "author": author, "content": content}
        )

    def generate_feedback(self):
        title = self.faker.sentence()
        content = self.faker.text(max_nb_chars=500)
        self.try_create_feedback({"title": title, "content": content})

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

    def try_create_friend_request(self, data):
        try:
            self.create_friend_request(data)
        except:
            pass

    def try_create_notification(self, data):
        try:
            self.create_notification(data)
        except:
            pass

    def try_create_message(self, data):
        try:
            return self.create_message(data)
        except:
            pass

    def try_create_conversation(self, data):
        try:
            self.create_conversation(data)
        except:
            pass

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

    def try_create_report(self, data):
        try:
            self.create_report(data)
        except:
            pass

    def try_create_post(self, data):
        try:
            self.create_post(data)
        except:
            pass

    def try_create_post_comment(self, data):
        try:
            self.create_post_comment(data)
        except:
            pass

    def try_create_feedback(self, data):
        try:
            self.create_feedback(data)
        except:
            pass

    def create_user(self, model, data):
        profile_picture = data.pop("profile_picture", None)
        user = model.objects.create(**data)
        if profile_picture:
            user.userprofile.profile_picture = profile_picture
            user.userprofile.save()
        user.set_password(Command.DEFAULT_PASSWORD)
        if data["username"] == "@johndoe":
            user.is_superuser = user.is_staff = True
        user.save()
        if model == Mentor:
            Referral.objects.create(referrer=user, code=data["referral_code"])
        return user

    def create_patient(self, data):
        self.create_user(Patient, data)

    def create_parent(self, data):
        self.create_user(Parent, data)

    def create_mentor(self, data):
        self.create_user(Mentor, data)

    def create_friend_request(self, data):
        sender = self.get_user(data["sender"])
        receiver = self.get_user(data["receiver"])
        FriendRequest.objects.create(sender=sender, receiver=receiver)

    def create_notification(self, data):
        data["user"] = self.get_user(data["user"]) ##
        Notification.objects.create(**data)

    def create_message(self, data):
        data["sender"] = self.get_user({"username": data["sender"]})
        message = Message.objects.create(**data)
        return message

    def create_conversation(self, data):
        users = [
            self.get_user({"username": username})
            for username in data["users"]["usernames"]
        ]
        conversation = Conversation.objects.create()
        message_objects = [self.create_message(message) for message in data["messages"]]
        for message_object in message_objects:
            message_object.visible_to.set(users)
        conversation.users.set(users)
        conversation.messages.set(message_objects)
        conversation.save()
        for user in users:
            user.conversations.add(conversation)

    def create_question(self, data):
        data["author"] = self.get_user(data["author"])
        Question.objects.create(**data)

    def create_response(self, data):
        data["user"] = self.get_user(data["user"])
        data["question"] = Question.objects.filter(
            title=data["question"]["title"]
        ).first()
        Response.objects.create(**data)

    def create_report(self, data):
        data["reporter"] = self.get_user(data["reporter"])
        if data["content_type"] == "User":
            data["object_id"] = self.get_user(data["object_id"]).pk
        elif data["content_type"] == "Message":
            data["object_id"] = self.get_message(data["object_id"]).pk
        data["content_type"] = self.get_content_type(data["content_type"].lower())
        Report.objects.create(**data)

    def create_post(self, data):
        data["author"] = self.get_user(data["author"])
        Post.objects.create(**data)

    def create_post_comment(self, data):
        data["post"] = self.get_post(data["post"])
        data["author"] = self.get_user(data["author"])
        PostComment.objects.create(**data)

    def create_feedback(self, data):
        Feedback.objects.create(**data)

    def get_message(self, data):
        return Message.objects.filter(sender=self.get_user(data["sender"]).pk).first()

    def get_user(self, data):
        return User.objects.get(username=data["username"])

    def get_content_type(self, model_name):
        return ContentType.objects.get(model=model_name)

    def get_post(self, data):
        return Post.objects.filter(content=data["content"]).first()


def create_username(first_name, last_name):
    return "@" + first_name.lower() + last_name.lower()


def create_email(first_name, last_name):
    return first_name + "." + last_name + "@example.org"
