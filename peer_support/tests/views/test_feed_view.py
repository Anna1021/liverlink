from django.test import TestCase
from django.urls import reverse
from peer_support.forms import PostForm
from peer_support.models import User, Post

class FeedViewTestCase(TestCase):
    """Tests of the feed view."""
    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_post.json',
        'peer_support/tests/fixtures/other_posts.json'
    ]

    def setUp(self):
        self.url = reverse('feed')
        self.user = User.objects.get(pk=1)
        self.user.friends.add(User.objects.get(pk=2))
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)
        
        self.user.friends.add(self.user2)
        self.user2.friends.add(self.user) 
        
        self.post = Post.objects.get(pk=1)
        self.friend_post = Post.objects.get(pk=2)
        self.friend_post.author = self.user2
        self.friend_post.save()

        self.stranger_post = Post.objects.get(pk=3)

        self.client.login(username=self.user.username, password="Password123")
    
    def test_create_post_url(self):
        self.assertEqual(self.url,'/feed/')
    
    def test_access_page_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('log_in') + "?next=" + self.url)

    def test_get_create_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PostForm))
        self.assertFalse(form.is_bound)
    
    def test_post_text_must_not_be_empty(self):
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

    def test_post_text_must_not_exceed_maximum_280_characters(self):
        form_input = {
            'text': 'A' * 281
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
    
    def test_post_valid_data(self):
        self.client.login(username=self.user.username, password='Password123')
        form_data = {
            'text': 'User post'
        }
        response = self.client.post(self.url, form_data)
        self.assertRedirects(response, reverse('feed'))

    def test_post_invalid_data(self):
        self.client.login(username=self.user.username, password='Password123')
        form_data = {
            'text': ''
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
        

    def test_global_feed_contains_all_posts(self):
        response = self.client.get(self.url + '?feed_type=global')
        self.assertContains(response, "User post")
        self.assertContains(response, "Friend post")
    
    def test_friends_feed_contains_friend_and_user_posts_only(self):
        response = self.client.get(self.url + '?feed_type=friends')
        self.assertContains(response, "User post")
        self.assertContains(response, "Friend post")
        self.assertNotContains(response, "Stranger post")    
