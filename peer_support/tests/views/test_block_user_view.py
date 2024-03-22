"""Tests of the block user view."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User, FriendRequest, Notification

class BlockUserViewTestCase(TestCase):
    """Tests of the block user view."""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.second_user = User.objects.get(username='@janedoe')
        self.url = reverse('block_user', args=[self.second_user.id])
        self.client.force_login(self.user)

    def test_block_user_url(self):
        self.assertEqual(self.url, '/block_user/2')

    def test_block_user(self):
        before_count = self.user.blocked_users.count()
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count = self.user.blocked_users.count()
        self.assertEqual(before_count + 1, after_count)
        self.assertIn(self.second_user, self.user.blocked_users.all())
        self.assertNotIn(self.user, self.second_user.blocked_users.all())

    def test_block_user_successfully_deletes_associated_friend_requests_from_blocking_user(self):
        friend_request = FriendRequest.objects.create(sender=self.user, receiver=self.second_user, is_accepted=False)
        before_friend_request_count = FriendRequest.objects.count()
        self.assertEqual(friend_request.sender, self.user)
        self.assertEqual(friend_request.receiver, self.second_user)
        self.test_block_user()
        final_friend_request_count = FriendRequest.objects.count()
        self.assertEqual(before_friend_request_count - 1, final_friend_request_count)
        self.assertFalse(FriendRequest.objects.filter(sender=self.user).filter(receiver=self.second_user).exists())

    def test_block_user_successfully_deletes_associated_friend_requests_from_blocked_user(self):
        friend_request = FriendRequest.objects.create(sender=self.second_user, receiver=self.user, is_accepted=False)
        before_friend_request_count = FriendRequest.objects.count()
        self.assertEqual(friend_request.sender, self.second_user)
        self.assertEqual(friend_request.receiver, self.user)
        self.test_block_user()
        final_friend_request_count = FriendRequest.objects.count()
        self.assertEqual(before_friend_request_count - 1, final_friend_request_count)
        self.assertFalse(FriendRequest.objects.filter(sender=self.second_user).filter(receiver=self.user).exists())

    def test_block_user_successfully_deletes_associated_notifications_from_blocking_user(self):
        url = reverse('send_friend_request', args=[self.second_user.id])
        self.assertEqual(url, '/send_friend_request/2')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FriendRequest.objects.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)
        friend_request = FriendRequest.objects.first()
        content_type_id = ContentType.objects.get_for_model(FriendRequest)
        notification = Notification.objects.get(content_type=content_type_id, object_id=friend_request.id)
        self.assertEqual(friend_request.sender, self.user)
        self.assertEqual(friend_request.receiver, self.second_user)
        self.assertEqual(notification.title, 'New Friend Request')
        self.assertEqual(notification.description, '@johndoe has sent you a friend request.')
        self.assertEqual(notification.user, self.second_user)
        self.assertEqual(notification.notifying_user, self.user)
        self.assertEqual(notification.content_type, content_type_id)
        self.assertEqual(notification.object_id, friend_request.id)
        self.assertEqual(notification.content_object, friend_request)
        self.test_block_user()
        self.assertEqual(FriendRequest.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)
        self.assertFalse(FriendRequest.objects.filter(sender=self.user).filter(receiver=self.second_user).exists())
        self.assertFalse(Notification.objects.filter(content_type=content_type_id, object_id=friend_request.id).exists())

    def test_block_user_successfully_deletes_associated_notifications_from_blocked_user(self):
        self.client.logout()
        self.client.force_login(self.second_user)
        url = reverse('send_friend_request', args=[self.user.id])
        self.assertEqual(url, '/send_friend_request/1')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FriendRequest.objects.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)
        friend_request = FriendRequest.objects.first()
        content_type_id = ContentType.objects.get_for_model(FriendRequest)
        notification = Notification.objects.get(content_type=content_type_id, object_id=friend_request.id)
        self.assertEqual(friend_request.sender, self.second_user)
        self.assertEqual(friend_request.receiver, self.user)
        self.assertEqual(notification.title, 'New Friend Request')
        self.assertEqual(notification.description, '@janedoe has sent you a friend request.')
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.notifying_user, self.second_user)
        self.assertEqual(notification.content_type, content_type_id)
        self.assertEqual(notification.object_id, friend_request.id)
        self.assertEqual(notification.content_object, friend_request)
        self.client.logout()
        self.client.force_login(self.user)
        self.test_block_user()
        self.assertEqual(FriendRequest.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)
        self.assertFalse(FriendRequest.objects.filter(sender=self.second_user).filter(receiver=self.user).exists())
        self.assertFalse(Notification.objects.filter(content_type=content_type_id, object_id=friend_request.id).exists())

    def test_block_user_successfully_removes_friend(self):
        before_friends_count = self.user.friends.count()
        self.user.friends.add(self.second_user)
        after_friends_count = self.user.friends.count()
        self.assertIn(self.second_user, self.user.friends.all())
        self.assertIn(self.user, self.second_user.friends.all())
        self.assertEqual(before_friends_count + 1, after_friends_count)
        self.test_block_user()
        self.user.refresh_from_db()
        final_friends_count = self.user.friends.count()
        self.assertNotIn(self.second_user, self.user.friends.all())
        self.assertNotIn(self.user, self.second_user.friends.all())
        self.assertEqual(before_friends_count, final_friends_count)

    def test_block_user_without_being_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
