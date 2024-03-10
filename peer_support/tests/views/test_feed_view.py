from django.test import TestCase
from django.urls import reverse
from peer_support.forms import PostForm
from peer_support.models import User, Post


class FeedViewTest(TestCase):
    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_post.json'
    ]

    def setUp(self):
        self.url = reverse('feed')
        self.user = User.objects.get(username='@johndoe')
        self.post = Post.objects.get(pk=1)
        self.client.login(username=self.user.username, password="Password123")
    
    def test_create_post_url(self):
        self.assertEqual(self.url,'/feed/')
    
    def test_get_create_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PostForm))
        self.assertFalse(form.is_bound)
    
    def test_unsuccessful_post_creation(self):
        form_input = {
            'text':''
        }
        before_count = Post.objects.count()
        response = self.client.post(self.url,data=form_input)
        after_count = Post.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PostForm))
        self.assertTrue(form.is_bound)

    def test_successful_direct_post_creation(self):
        form_input = {
            'text':'Test post creation'
        }
        before_count = Post.objects.count()
        response = self.client.post(self.url, data=form_input,follow=True)
        after_count = Post.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertTemplateUsed(response, 'feed.html')
        self.assertRedirects(response, reverse('feed'),  status_code=302, target_status_code=200)
