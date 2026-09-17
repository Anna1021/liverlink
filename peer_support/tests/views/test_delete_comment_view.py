"""Tests of the comment deletion view"""
from django.test import TestCase
from django.urls import reverse
from peer_support.models import Post,PostComment,User
from django.contrib import messages

class DeletePostViewTestCase(TestCase):
    """Tests of the comment deletion view"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_post.json',
        'peer_support/tests/fixtures/other_posts.json',
        'peer_support/tests/fixtures/default_post_comment.json',
        'peer_support/tests/fixtures/other_comments.json',
    ]

    def setUp(self):
        self.post = Post.objects.get(pk=1)
        self.comment = PostComment.objects.get(pk=1)
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('delete_comment', kwargs={'comment_id':self.comment.id})

    def test_delete_comment_url(self):
        self.assertEqual(self.url, '/delete_comment/1')

    def test_successful_delete_comment(self):
        posts_before = PostComment.objects.count()
        response = self.client.get(self.url, follow=True)
        posts_after = PostComment.objects.count()
        self.assertEqual(posts_after + 2, posts_before)
        redirect_url = reverse('post',kwargs={'post_id':self.post.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'post.html')

    def test_cannot_delete_nonexistent_comment(self):
        invalid_url = reverse('delete_comment',kwargs={'comment_id':3})
        posts_before = PostComment.objects.count()
        response = self.client.get(invalid_url, follow=True)
        posts_after = PostComment.objects.count()
        self.assertEqual(posts_after, posts_before)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
    
    def test_cannot_delete_comment_on_non_visible_post(self):
        self.post.author = User.objects.get(username='@janedoe')
        self.post.visibility = 'F'
        self.post.save()
        posts_before = PostComment.objects.count()
        response = self.client.get(self.url, follow=True)
        posts_after = PostComment.objects.count()
        self.assertEqual(posts_after, posts_before)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_unauthorized_delete_comment(self):
        self.client.logout()
        unauthorized_user = User.objects.get(username='@janedoe')
        self.client.login(username=unauthorized_user.username, password='Password123')
        posts_before = PostComment.objects.count()
        response = self.client.get(self.url, follow=True)
        posts_after = PostComment.objects.count()
        self.assertEqual(posts_after, posts_before)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)