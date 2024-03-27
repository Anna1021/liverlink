from random import randint
from peer_support.management.commands.helpers import get_user, get_post
from peer_support.management.commands.seeders.parent_seeder import parent_fixtures
from peer_support.management.commands.seeders.patient_seeder import patient_fixtures
from peer_support.management.commands.seeders.mentor_seeder import mentor_fixtures
from peer_support.management.commands.seeders.post_seeder import post_fixtures
from peer_support.models import PostComment, Post, User

post_comment_fixtures = [
    {"post": post_fixtures[0], "author": parent_fixtures[0], "content": "This is my comment."},
    {"post": post_fixtures[1], "author": patient_fixtures[0], "content": "Hello!"},
    {"post": post_fixtures[2], "author": mentor_fixtures[0], "content": "Hi, I am a mentor."},
]

class PostCommentSeeder:
    """Seed post comments into the database."""

    POST_COMMENT_COUNT = 1000

    def __init__(self, faker):
        self.faker = faker
        self.users = User.objects.all()
        self.posts = Post.objects.all()

    def create_post_comments(self):
        self.generate_post_comment_fixtures()
        self.generate_random_post_comments()

    def generate_post_comment_fixtures(self):
        for data in post_comment_fixtures:
            self.try_create_post_comment(data)

    def generate_random_post_comments(self):
        post_comment_count = PostComment.objects.count()
        while post_comment_count < self.POST_COMMENT_COUNT:
            print(f"Seeding post comment {post_comment_count}/{self.POST_COMMENT_COUNT}", end="\r")
            self.generate_post_comment()
            post_comment_count = PostComment.objects.count()
        print("Post comment seeding complete.      ")

    def generate_post_comment(self):
        post = self.posts[randint(0, len(self.posts) - 1)]
        author = self.users[randint(0, len(self.users) - 1)]
        content = self.faker.text(max_nb_chars=255)
        post = {"content": post.content}
        author = {"username": author.username}
        self.try_create_post_comment(
            {"post": post, "author": author, "content": content}
        )

    def try_create_post_comment(self, data):
        try:
            self.create_post_comment(data)
        except:
            pass

    def create_post_comment(self, data):
        data["post"] = get_post(data["post"])
        data["author"] = get_user(data["author"])
        PostComment.objects.create(**data)
