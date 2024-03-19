"""Tests of the post deletion view"""
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
    ]

    def setUp(self):
        self.post = Post.objects.get(pk=1)
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('delete_post', kwargs={'post_id':self.post.id})

    def test_delete_post_url(self):
        self.assertEqual(self.url, '/delete_post/1')

    def test_successful_delete_post(self):
        posts_before = Post.objects.count()
        response = self.client.get(self.url, follow=True)
        posts_after = Post.objects.count()
        self.assertEqual(posts_after + 1, posts_before)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_cannot_delete_nonexistent_post(self):
        invalid_url = reverse('delete_post',kwargs={'post_id':2})
        posts_before = Post.objects.count()
        response = self.client.get(invalid_url, follow=True)
        posts_after = Post.objects.count()
        self.assertEqual(posts_after, posts_before)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_unauthorized_delete_post(self):
        self.client.logout()
        unauthorized_user = User.objects.get(username='@janedoe')
        self.client.login(username=unauthorized_user.username, password='Password123')
        posts_before = Post.objects.count()
        response = self.client.get(self.url, follow=True)
        posts_after = Post.objects.count()
        self.assertEqual(posts_after, posts_before)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)