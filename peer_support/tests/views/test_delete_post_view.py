"""Tests for the post deletion view"""
from django.test import TestCase
from django.urls import reverse
from peer_support.models import Post,User
from django.contrib import messages

class DeletePostViewTestCase(TestCase):
    """Tests of the post deletion view"""
    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_post.json',
        'peer_support/tests/fixtures/other_posts.json'
    ]
    def setUp(self):
        self.post = Post.objects.get(pk=1)
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('delete_post',kwargs={'post_id':self.post.id,'post_id':self.post.id})

        self.post.author = self.user
        self.post.save()

    def test_delete_post_url(self):
        self.assertEqual(self.url,'/delete_post/1')

    def test_successful_delete_post(self):
        posts_before = Post.objects.count()
        response = self.client.get(self.url,follow=True)
        posts_after = Post.objects.count()
        self.assertEqual(posts_after + 1,posts_before)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
    """
    def test_unauthorized_delete_post(self):
        unauthorized_user = User.objects.create(username='@authorizeduser', password='Password123')
        self.client.login(username=unauthorized_user.username, password='Password123')
        posts_before = Post.objects.count()
        response = self.client.get(self.url, follow=True)
        posts_after = Post.objects.count()
        self.assertEqual(posts_after, posts_before)
        self.assertContains(response, "You are not authorized to delete this post.")
    """