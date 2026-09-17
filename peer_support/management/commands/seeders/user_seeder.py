from django.contrib.auth.hashers import make_password
from peer_support.models import User, Mentor, Professional, Referral
from peer_support.models.model_choices import *
from random import randint


class UserSeeder:
    """Handle common user data"""

    DEFAULT_PASSWORD = "Password123"
    default_password_hash = None

    def __init__(self, faker):
        self.faker = faker
        self.users = User.objects.all()
        if UserSeeder.default_password_hash is None:
            UserSeeder.default_password_hash = make_password(self.DEFAULT_PASSWORD)

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
        return {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "location": location,
            "hospital": hospital,
            "ethnicity": ethnicity,
            "language": language,
            "bio": bio,
            "profile_picture": profile_picture,
        }
    
    def create_user(self, model, data):
        profile_picture = data.pop("profile_picture", None)
        user = model.objects.create(**data)
        if profile_picture:
            user.userprofile.profile_picture = profile_picture
            user.userprofile.save()
        # Every seeded account uses the same documented test password. Reuse
        # one secure hash so creating hundreds of demo users remains fast.
        user.password = self.default_password_hash
        if data["username"] == "@johndoe":
            user.is_superuser = user.is_staff = True
        user.save()
        if model == Mentor or model == Professional:
            Referral.objects.create(referrer=user, code=data['referral_code'])
        return user
    
    def seed_friends(self):
        print("Seeding friends...", end='\r')
        for user in self.users:
            friends_count = user.friends.count()
            if friends_count >= 10:
                continue
            for _ in range(1, 10):
                friend = self.users[randint(0, len(self.users) - 1)]
                if friend != user and friend not in user.friends.all():
                    user.friends.add(friend)

    def seed_blocked_users(self):
        print("Seeding blocked users...", end='\r')
        for user in self.users:
            blocked_user_count = user.blocked_users.count()
            if blocked_user_count >= 10:
                continue
            for _ in range(1, 10):
                blocked_user = self.users[randint(0, len(self.users) - 1)]
                if blocked_user != user and blocked_user not in user.friends.all() and blocked_user not in user.blocked_users.all():
                    user.blocked_users.add(blocked_user)

def create_username(first_name, last_name):
    return "@" + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
    return first_name + "." + last_name + "@example.org"
