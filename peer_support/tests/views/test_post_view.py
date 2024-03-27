"""Tests of the post view."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from peer_support.models import User, Post, PostComment, Report, Notification
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
        self.url = reverse('post', kwargs={'post_id': self.post.id})
        self.redirect_url = reverse('feed')
        self.reply = PostComment.objects.get(pk=2)
        self.client.login(username=self.user.username, password='Password123')

        self.comment_input_data = {
            'content': 'User comment',
            'post': self.post.id,
        }
    
    def test_get_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_cannot_get_nonexistent_post(self):
        invalid_url = reverse('post',kwargs={'post_id':4})
        response = self.client.get(invalid_url,follow=True)
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed('feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_cannot_get_post_of_blocked_user(self):
        invalid_url = reverse('post',kwargs={'post_id':3})
        self.user.blocked_users.add(User.objects.get(id=3))
        response = self.client.get(invalid_url,follow=True)
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed('feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_cannot_get_post_of_blocked_by_user(self):
        invalid_url = reverse('post',kwargs={'post_id':3})
        blocking_user = User.objects.get(id=3)
        blocking_user.blocked_users.add(self.user)
        response = self.client.get(invalid_url,follow=True)
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed('feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_cannot_get_private_post_of_non_friend(self):
        invalid_url = reverse('post',kwargs={'post_id':5})
        response = self.client.get(invalid_url,follow=True)
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed('feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
    
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

    def test_valid_comment_creation_sends_notification_to_post_author(self):
        self.client.logout()
        replying_user = User.objects.get(id=3)
        self.client.force_login(replying_user)
        response_count_before = PostComment.objects.count()
        notification_count_before = Notification.objects.count()
        self.client.post(self.url, self.comment_input_data)
        response_count_after = PostComment.objects.count()
        notification_count_after = Notification.objects.count()
        self.assertEqual(response_count_after, response_count_before + 1)
        self.assertEqual(notification_count_after, notification_count_before + 1)
        new_comment = PostComment.objects.latest('id')
        content_type_id = ContentType.objects.get_for_model(PostComment)
        notification = Notification.objects.get(content_type=content_type_id, object_id = new_comment.id)
        self.assertEqual(notification.title, "New Post Comment")
        self.assertEqual(notification.description, "@petrapickles has commented on your post.")
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.notifying_user, replying_user)
        self.assertEqual(notification.content_type, content_type_id)
        self.assertEqual(notification.object_id, new_comment.id)
        self.assertEqual(notification.content_object, new_comment)

    def test_valid_comment_creation_does_not_send_notification_if_authors_are_same(self):
        response_count_before = PostComment.objects.count()
        notification_count_before = Notification.objects.count()
        self.client.post(self.url, self.comment_input_data)
        response_count_after = PostComment.objects.count()
        notification_count_after = Notification.objects.count()
        self.assertEqual(response_count_after, response_count_before + 1)
        self.assertEqual(notification_count_after, notification_count_before)
        new_comment = PostComment.objects.latest('id')
        self.assertEqual(new_comment.author, new_comment.post.author)

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

    def test_valid_reply_creation_sends_notification_to_parent_and_post_authors(self):
        self.client.logout()
        replying_user = User.objects.get(id=3)
        self.client.force_login(replying_user)
        self.comment_input_data["parent_id"] = self.comment.id
        self.comment.author = User.objects.get(id=2)
        response_count_before = PostComment.objects.count()
        notification_count_before = Notification.objects.count()
        self.client.post(self.url, self.comment_input_data)
        response_count_after = PostComment.objects.count()
        notification_count_after = Notification.objects.count()
        self.assertEqual(response_count_after, response_count_before + 1)
        self.assertEqual(notification_count_after, notification_count_before + 2)
        new_comment = PostComment.objects.latest('id')
        content_type_id = ContentType.objects.get_for_model(PostComment)
        self.assertEqual(Notification.objects.filter(content_type=content_type_id, object_id = new_comment.id).count(), 2)

    def test_valid_reply_creation_does_not_send_notification_if_authors_are_same(self):
        self.comment_input_data["parent_id"] = self.comment.id
        response_count_before = PostComment.objects.count()
        notification_count_before = Notification.objects.count()
        self.client.post(self.url, self.comment_input_data)
        response_count_after = PostComment.objects.count()
        notification_count_after = Notification.objects.count()
        self.assertEqual(response_count_after, response_count_before + 1)
        self.assertEqual(notification_count_after, notification_count_before)
        new_comment = PostComment.objects.latest('id')
        self.assertEqual(new_comment.author, new_comment.post.author)
        self.assertEqual(new_comment.author, new_comment.parent.author)
        
    def test_invalid_comment_creation(self):
        response_count_before = PostComment.objects.count()
        self.comment_input_data['content']=''
        response = self.client.post(self.url, data=self.comment_input_data)
        response_count_after = PostComment.objects.count()
        self.assertEqual(response_count_after, response_count_before)
        self.assertRedirects(response, self.url, status_code=302, target_status_code=200)
        
    def test_report_comment_valid(self):
        initial_report_count = Report.objects.count()
        form_data = {
            'report_comment': True,
            'action': self.comment.id,
            'reason': 'abuse'
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        final_report_count = Report.objects.count()
        self.assertEqual(final_report_count, initial_report_count + 1)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertIn("Comment reported successfully.", str(messages_list[0]))

    def test_report_post_valid(self):
        initial_report_count = Report.objects.count()
        form_data = {
            'report_post': True,
            'action': self.post.id,
            'reason': 'abuse'
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        final_report_count = Report.objects.count()
        self.assertEqual(final_report_count, initial_report_count + 1)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertIn("Post reported successfully.", str(messages_list[0]))

    def test_report_comment_invalid_reason(self):
        initial_report_count = Report.objects.count()
        form_data = {
            'report_comment': True,
            'action': self.comment.id,
            'reason': 'dgfdd' 
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        final_report_count = Report.objects.count()
        self.assertEqual(final_report_count, initial_report_count)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertIn("There was an issue with the report.", str(messages_list[0]))

    def test_report_post_invalid_reason(self):
        initial_report_count = Report.objects.count()
        form_data = {
            'report_post': True,
            'action': self.post.id,
            'reason': 'dgfdd' 
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        final_report_count = Report.objects.count()
        self.assertEqual(final_report_count, initial_report_count)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertIn("There was an issue with the post.", str(messages_list[0]))

