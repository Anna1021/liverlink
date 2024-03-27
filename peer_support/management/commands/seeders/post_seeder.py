from random import randint
from peer_support.management.commands.helpers import get_user
from peer_support.management.commands.seeders.parent_seeder import parent_fixtures
from peer_support.management.commands.seeders.patient_seeder import patient_fixtures
from peer_support.management.commands.seeders.mentor_seeder import mentor_fixtures
from peer_support.models import Post, User

post_fixtures = [
    {
        "author": patient_fixtures[0],
        "content": "This is my post",
        "likes": [parent_fixtures[0], mentor_fixtures[0]],
    },
    {
        "author": parent_fixtures[0],
        "content": "Hello world!",
        "likes": [patient_fixtures[0]],
        "visibility": "F",
    },
    {
        "author": mentor_fixtures[0],
        "content": "Hello, I am a mentor.",
        "likes": [patient_fixtures[1], parent_fixtures[1]],
    },
]

class PostSeeder:
    """Seed posts into the database."""

    POST_COUNT = 500

    def __init__(self, faker):
        self.faker = faker
        self.users = User.objects.all()

    def create_posts(self):
        self.generate_post_fixtures()
        self.generate_random_posts()

    def generate_post_fixtures(self):
        for data in post_fixtures:
            self.try_create_post(data)

    def generate_random_posts(self):
        post_count = Post.objects.count()
        while post_count < self.POST_COUNT:
            print(f"Seeding post {post_count}/{self.POST_COUNT}", end="\r")
            self.generate_post()
            post_count = Post.objects.count()
        print("Post seeding complete.      ")

    def generate_post(self):
        author = self.users[randint(0, len(self.users) - 1)]
        content = self.faker.text(max_nb_chars=280)
        likes = [self.users[randint(0, len(self.users) - 1)] for _ in range(randint(0, 100))]
        visibility = self.faker.random_element(elements=("G", "F"))
        author = {"username": author.username}
        likes = [{"username": like.username} for like in likes]
        self.try_create_post(
            {
                "author": author,
                "content": content,
                "likes": likes,
                "visibility": visibility,
            }
        )

    def try_create_post(self, data):
        try:
            self.create_post(data)
        except:
            pass

    def create_post(self, data):
        data["author"] = get_user(data["author"])
        likes = [get_user({"username": like["username"]}) for like in data["likes"]]
        data.pop("likes")
        post = Post.objects.create(**data)
        post.likes.set(likes)
        post.save()