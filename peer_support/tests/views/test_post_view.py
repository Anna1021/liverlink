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
        'peer_support/tests/fixtures/other_posts.json',
        'peer_support/tests/fixtures/default_comment.json',
        'peer_support/tests/fixtures/other_comments.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.post = Post.objects.get(pk=1)
        self.comment = PostComment.objects.get(pk=1)
        self.url = reverse('post_detail', kwargs={'post_id': self.post.id})
        self.reply = PostComment.objects.get(pk=2)
        self.client.login(username=self.user.username, password='Password123')

        self.comment_input_data = {
            'content': 'User comment',
            'post': self.post.id,
        }
    
    def test_get_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_valid_comment_creation(self):
        response_count_before = PostComment.objects.count()
        response = self.client.post(self.url, self.comment_input_data)
        response_count_after = PostComment.objects.count()
        self.assertEqual(response_count_after, response_count_before + 1)
        new_comment = PostComment.objects.latest('id')
        self.assertEqual(new_comment.parent, None)
        self.assertRedirects(response, self.url, status_code=302, target_status_code=200)
        self.assertEqual(new_comment.content, self.comment_input_data['content'])
        self.assertEqual(new_comment.author, self.user)
        self.assertEqual(new_comment.post, self.post)

    def test_valid_reply_creation(self):
        self.comment_input_data["parent_id"] = self.comment.id
        response_count_before = PostComment.objects.count()
        response = self.client.post(self.url, self.comment_input_data)
        response_count_after = PostComment.objects.count()
        self.assertEqual(response_count_after, response_count_before + 1)
        new_comment = PostComment.objects.latest('id')
        self.assertEqual(new_comment.parent, self.comment)
        self.assertRedirects(response, self.url, status_code=302, target_status_code=200)
        self.assertEqual(new_comment.content, self.comment_input_data['content'])
        self.assertEqual(new_comment.author, self.user)
        self.assertEqual(new_comment.post, self.post)
        
    def test_invalid_comment_creation(self):
        response_count_before = PostComment.objects.count()
        invalid_comment_form_data = {
            'content': '', 
            'post': self.post.id,
        }
        response = self.client.post(self.url, data=invalid_comment_form_data)
        response_count_after = PostComment.objects.count()
        self.assertEqual(response_count_after, response_count_before)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html')
        self.assertIn('form', response.context)
        form = response.context['comment_form']
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)  
        self.assertEqual(form.errors['content'], ['This field is required.'])

