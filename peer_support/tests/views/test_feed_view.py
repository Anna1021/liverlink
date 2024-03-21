"""Tests of the feed view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.forms import PostForm
from peer_support.models import User, Post
from django.contrib import messages

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
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)
        
        self.user.friends.add(self.user2)
        
        self.post = Post.objects.get(pk=1)
        self.friend_post = Post.objects.get(pk=2)
        self.stranger_post = Post.objects.get(pk=3)

        self.client.login(username=self.user.username, password="Password123")

        self.form_input={
            'visibility':'G',
            'content':'Test post'
        }
    
    def test_feed_url(self):
        self.assertEqual(self.url,'/feed/')
    
    def test_access_page_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('log_in') + "?next=" + self.url)

    def test_get_feed_first_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PostForm))
        self.assertFalse(form.is_bound)
        self.assertIn('first',response.context)
    
    def test_get_feed_not_first_log_in(self):
        self.user.first_login = False
        self.user.save()
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PostForm))
        self.assertFalse(form.is_bound)
        self.assertNotIn('first',response.context)
    
    def test_post_text_must_not_be_empty(self):
        self.form_input['content'] = ''
        before_count = Post.objects.count()
        response = self.client.post(self.url,data=self.form_input)
        after_count = Post.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PostForm))
        self.assertTrue(form.is_bound)

    def test_post_text_must_not_exceed_maximum_280_characters(self):
        self.form_input['content'] = 'A' * 281
        before_count = Post.objects.count()
        response = self.client.post(self.url,data=self.form_input)
        after_count = Post.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PostForm))
        self.assertTrue(form.is_bound)
    
    def test_post_valid_data(self):
        response = self.client.post(self.url, self.form_input)  
        self.assertRedirects(response, reverse('feed'))    

    def test_global_feed_contains_global_and_friends_posts(self):
        response = self.client.get(self.url + '?feed_type=global')
        self.assertContains(response, "User post")
        self.assertContains(response, "Friend post")
        self.assertContains(response, "Stranger post global")
        self.assertNotContains(response,"Stranger post friends")
    
    def test_friends_feed_contains_friend_and_user_posts_only(self):
        response = self.client.get(self.url + '?feed_type=friends')
        self.assertContains(response, "User post")
        self.assertContains(response, "Friend post")
        self.assertNotContains(response, "Stranger post global")    
        self.assertNotContains(response, "Stranger post friends")  

    def test_report_post_valid(self):
        report_data = {
            'report_post': True,
            'action': self.friend_post.pk, 
            'reason': 'spam' 
        }
        response = self.client.post(self.url, report_data, follow=True)
        self.assertRedirects(response, self.url)
        updated_post = Post.objects.get(pk=self.friend_post.pk)
        messages_list = [m.message for m in messages.get_messages(response.wsgi_request)]
        self.assertIn("Post reported successfully.", messages_list)

    def test_report_post_invalid(self):
        report_data = {
            'report_post': True,
            'action': self.friend_post.pk,
            'reason': 'Sphjgyjgham'
        }
        response = self.client.post(self.url, report_data, follow=True)
        self.assertRedirects(response, self.url)
        messages_list = [m.message for m in messages.get_messages(response.wsgi_request)]
        self.assertIn("There was an issue with the report.", messages_list)
