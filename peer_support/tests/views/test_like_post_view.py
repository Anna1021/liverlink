"""Tests for the like post view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User, Post


class LikePostViewTestCase(TestCase):
    """Tests for the like post view."""

    fixtures = [
        "peer_support/tests/fixtures/default_user.json",
        "peer_support/tests/fixtures/other_users.json",
        "peer_support/tests/fixtures/default_post.json",
    ]

    def setUp(self):
        self.url = reverse("like_post", args=[1])
        self.user = User.objects.get(username="@johndoe")
        self.client.force_login(self.user)

    def test_like_post_url(self):
        self.assertEqual(self.url, "/like_post/1")

    def test_like_post(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.likes.count(), 0)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.likes.count(), 1)

    def test_unlike_post(self):
        post = Post.objects.get(id=1)
        post.likes.add(self.user)
        self.assertEqual(post.likes.count(), 1)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.likes.count(), 0)

    def test_like_post_without_being_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next("log_in", self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertEqual(Post.objects.get(id=1).likes.count(), 0)
