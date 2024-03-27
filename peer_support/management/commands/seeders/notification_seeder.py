from random import randint
import random
from peer_support.management.commands.helpers import get_user, get_content_type
from peer_support.management.commands.seeders.parent_seeder import parent_fixtures
from peer_support.management.commands.seeders.patient_seeder import patient_fixtures
from peer_support.management.commands.seeders.mentor_seeder import mentor_fixtures
from peer_support.management.commands.seeders.post_comment_seeder import post_comment_fixtures
from peer_support.management.commands.seeders.response_seeder import response_fixtures
from peer_support.models import PostComment, User, Notification, Response, PostComment, FriendRequest, Post

notification_fixtures = [
    {
        "title": "Welcome to Peer Support",
        "description": "Welcome to Peer Support. We are glad to have you here.",
        "user": patient_fixtures[0],
    },
    {
        "user": patient_fixtures[0],
        "notifying_user": mentor_fixtures[0],
        "content_type": "response",
        "object_id": response_fixtures[0],
    },
    {
        "user": patient_fixtures[0],
        "notifying_user": parent_fixtures[0],
        "content_type": "postcomment",
        "object_id": post_comment_fixtures[0],
    },
]


class NotificationSeeder:
    """Seed notifications into the database."""

    NOTIFICATION_COUNT = 500

    def __init__(self, faker):
        self.faker = faker
        self.users = User.objects.all()
        self.posts = Post.objects.all()
        self.friend_requests = FriendRequest.objects.all()
        self.responses = Response.objects.all()
        self.post_comments = PostComment.objects.all()

    def create_notifications(self):
        self.generate_notification_fixtures()
        self.generate_random_notifications()

    def generate_notification_fixtures(self):
        for data in notification_fixtures:
            self.try_create_notification(data)

    def generate_random_notifications(self):
        notification_count = Notification.objects.count()
        while notification_count < self.NOTIFICATION_COUNT:
            print(f"Seeding notification {notification_count}/{self.NOTIFICATION_COUNT}", end="\r")
            self.generate_notification()
            notification_count = Notification.objects.count()
        print("Notification seeding complete.      ")

    def generate_notification(self):
        user = self.users[randint(0, len(self.users) - 1)]
        if self.friend_requests.filter(receiver=user) and random.choice([True, False]):
            self.generate_friend_request_notification(user)
        elif self.post_comments.filter(post__author=user) and random.choice([True, False]):
            self.generate_post_comment_notification(user)
        elif self.responses.filter(question__author=user) and random.choice([True, False]):
            self.generate_question_response_notification(user)
        elif self.posts.filter(author=user, likes__gte=1) and random.choice([True, False]):
            self.generate_post_like_notification(user)
        else:
            title = self.faker.sentence()
            description = self.faker.text(max_nb_chars=100)
            user = {"username": user.username}
            self.try_create_notification({"title": title, "description": description, "user": user})

    def generate_friend_request_notification(self, user):
        friend_request = random.choice(self.friend_requests.filter(receiver=user))
        user = {"username": user.username}
        notifying_user = {"username": friend_request.sender.username}
        content_type = "friendrequest"
        object_id = {"sender": get_user(notifying_user), "receiver": get_user(user)}
        self.try_create_notification({"user": user, "notifying_user": notifying_user,
                                    "content_type": content_type, "object_id": object_id})

    def generate_post_comment_notification(self, user):
        post_comment = random.choice(self.post_comments.filter(post__author=user))
        notifying_user = {"username": post_comment.author.username}
        user = {"username": user.username}
        content_type = "postcomment"
        object_id = {"content": post_comment.content}
        self.try_create_notification({"user": user, "notifying_user": notifying_user,
                                    "content_type": content_type, "object_id": object_id})

    def generate_question_response_notification(self, user):
        response = random.choice(self.responses.filter(question__author=user))
        notifying_user = {"username": response.user.username}
        user = {"username": user.username}
        content_type = "response"
        object_id = {"body": response.body}
        self.try_create_notification({"user": user, "notifying_user": notifying_user,
                                    "content_type": content_type, "object_id": object_id})

    def generate_post_like_notification(self, user):
        post = random.choice(self.posts.filter(author=user, likes__gte=1))
        notifying_user = {"username": random.choice(post.likes.exclude(id=user.id)).username}
        user = {"username": user.username}
        content_type = "post"
        object_id = {"content": post.content}
        title = "New Post Like"
        self.try_create_notification({"user": user, "notifying_user": notifying_user, "title": title,
                                          "content_type": content_type, "object_id": object_id})

    def try_create_notification(self, data):
        try:
            self.create_notification(data)
        except:
            pass

    def create_notification(self, data):
        data["user"] = get_user(data["user"])
        if data.get("content_type"):
            ids = {"postcomment": self.post_comments.filter(content=data["object_id"].get("content", None)),
            "response": self.responses.filter(body=data["object_id"].get("body", None)),
            "post": self.posts.filter(content=data["object_id"].get("content", None)),
            "friendrequest": self.friend_requests.filter(sender=data["object_id"].get("sender", None),
                                                          receiver=data["object_id"].get("receiver", None))}
            data["notifying_user"] = get_user(data["notifying_user"])
            data["object_id"] = ids[data["content_type"]].first().id
            data["content_type"] = get_content_type(data["content_type"])
            exists = Notification.objects.filter(content_type=data["content_type"], object_id=data["object_id"]).exists()
            if exists: Exception
        Notification.objects.create(**data)