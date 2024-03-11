from django.test import TestCase
from django.urls import reverse
from peer_support.forms import PostForm
from peer_support.models import User, Post, PostComment
from django.contrib import messages

class PostViewTestCase(TestCase):
    """Tests of the post view."""
    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_post.json',
        'peer_support/tests/fixtures/other_posts.json'
    ]
    def setUp(self):
        pass