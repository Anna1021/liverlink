from random import randint
from peer_support.management.commands.helpers import get_user
from peer_support.management.commands.seeders.parent_seeder import parent_fixtures
from peer_support.management.commands.seeders.patient_seeder import patient_fixtures
from peer_support.models import FriendRequest, User

friend_request_fixtures = [
    {"sender": patient_fixtures[0], "receiver": parent_fixtures[0]},
    {"sender": parent_fixtures[0], "receiver": patient_fixtures[0]},
    {"sender": patient_fixtures[1], "receiver": parent_fixtures[1]},
]

class FriendRequestSeeder:
    """Seed friend requests into the database."""

    FRIEND_REQUEST_COUNT = 100

    def __init__(self, faker):
        self.faker = faker
        self.users = User.objects.all()

    def create_friend_requests(self):
        self.generate_friend_request_fixtures()
        self.generate_random_friend_requests()

    def generate_friend_request_fixtures(self):
        for data in friend_request_fixtures:
            self.try_create_friend_request(data)

    def generate_random_friend_requests(self):
        friend_request_count = FriendRequest.objects.count()
        while friend_request_count < self.FRIEND_REQUEST_COUNT:
            print(f"Seeding friend request {friend_request_count}/{self.FRIEND_REQUEST_COUNT}", end='\r')
            self.generate_friend_request()
            friend_request_count = FriendRequest.objects.count()
        print("Friend request seeding complete.      ")

    def generate_friend_request(self):
        sender = self.users[randint(0, len(self.users) - 1)]
        receiver = self.users[randint(0, len(self.users) - 1)]
        sender = {"username": sender.username}
        receiver = {"username": receiver.username}
        self.try_create_friend_request({"sender": sender, "receiver": receiver})

    def try_create_friend_request(self, data):
        try:
            self.create_friend_request(data)
        except:
            pass

    def create_friend_request(self, data):
        sender = get_user(data["sender"])
        receiver = get_user(data["receiver"])
        FriendRequest.objects.create(sender=sender, receiver=receiver)