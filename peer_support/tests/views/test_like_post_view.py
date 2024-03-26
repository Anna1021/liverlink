"""Tests for the like post view."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User, Post, Notification


class LikePostViewTestCase(TestCase):
    """Tests for the like post view."""

    fixtures = [
        "peer_support/tests/fixtures/default_user.json",
        "peer_support/tests/fixtures/default_post.json",
        "peer_support/tests/fixtures/other_users.json"
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
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.likes.count(), 1)

    def test_like_post_sends_notification(self):
        post = Post.objects.get(id=1)
        post_author = User.objects.get(id=2)
        post.author = post_author
        post.save()
        self.assertEqual(post.likes.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.likes.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)
        new_notification = Notification.objects.first()
        content_type = ContentType.objects.get_for_model(Post)
        self.assertEqual(new_notification.title, "New Post Like")
        self.assertEqual(new_notification.description, "@johndoe has liked your post.")
        self.assertEqual(new_notification.user, post_author)
        self.assertEqual(new_notification.notifying_user, self.user)
        self.assertEqual(new_notification.content_type, content_type)
        self.assertEqual(new_notification.object_id, post.id)
        self.assertEqual(new_notification.content_object, post)

    def test_like_post_does_not_send_notification_if_notification_already_exists(self):
        self.test_like_post_sends_notification()
        post = Post.objects.get(id=1)
        post.likes.remove(self.user)
        self.assertEqual(post.likes.count(), 0)
        self.assertEqual(Notification.objects.count(), 1)
        before_notification = Notification.objects.first()
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.likes.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)
        after_notification = Notification.objects.last()
        self.assertEqual(before_notification, after_notification)

    def test_like_post_does_not_send_notification_if_user_likes_own_post(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.likes.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.likes.count(), 1)
        self.assertEqual(Notification.objects.count(), 0)
        self.assertIn(post.author, post.likes.all())

    def test_unlike_post(self):
        post = Post.objects.get(id=1)
        post.likes.add(self.user)
        self.assertEqual(post.likes.count(), 1)
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.likes.count(), 0)

    def test_like_post_only_allows_post_requests(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 405)

    def test_like_post_without_being_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next("log_in", self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertEqual(Post.objects.get(id=1).likes.count(), 0)
