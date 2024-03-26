"""Unit tests for the Notification model."""
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from peer_support.models import User, Notification, FriendRequest, GroupConversation, Conversation, Post, PostComment, Question, Response

class NotificationModelTestCase(TestCase):
    """Unit tests for the Notification model."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_notification.json',
        'peer_support/tests/fixtures/other_notifications.json',
        'peer_support/tests/fixtures/default_friend_request.json',
        'peer_support/tests/fixtures/default_conversation.json',
        'peer_support/tests/fixtures/default_message.json',
        'peer_support/tests/fixtures/other_messages.json',
        'peer_support/tests/fixtures/default_group_conversation.json',
        'peer_support/tests/fixtures/default_post.json',
        'peer_support/tests/fixtures/default_post_comment.json',
        'peer_support/tests/fixtures/default_question.json',
        'peer_support/tests/fixtures/default_response.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.second_user = User.objects.get(username='@janedoe')
        self.basic_notification = Notification.objects.get(id=1)
        self.object_notification = Notification.objects.get(id=2)

    def test_valid_basic_notification(self):
        self._assert_basic_notification_is_valid()

    def test_valid_object_notification(self):
        self._assert_object_notification_is_valid()


    def test_title_cannot_be_blank(self):
        self.basic_notification.title = ''
        self._assert_basic_notification_is_invalid()

    def test_title_can_be_100_characters_long(self):
        self.basic_notification.title = 'x' * 100
        self._assert_basic_notification_is_valid()

    def test_title_cannot_be_over_100_characters_long(self):
        self.basic_notification.title = 'x' * 101
        self._assert_basic_notification_is_invalid()


    def test_description_cannot_be_blank(self):
        self.basic_notification.description = ''
        self._assert_basic_notification_is_invalid()

    def test_description_can_be_1000_characters_long(self):
        self.basic_notification.description = 'x' * 1000
        self._assert_basic_notification_is_valid()

    def test_description_cannot_be_over_1000_characters_long(self):
        self.basic_notification.description = 'x' * 1001
        self._assert_basic_notification_is_invalid()


    def test_created_defaults_to_now(self):
        new_notification = Notification.objects.create(user=self.user, title="Test", description="Test")
        self.assertIsNotNone(new_notification.created)


    def test_viewed_defaults_to_false(self):
        new_notification = Notification.objects.create(user=self.user, title="Test", description="Test")
        self.assertFalse(new_notification.viewed)


    def test_user_cannot_be_blank(self):
        self.basic_notification.user = None
        self._assert_basic_notification_is_invalid()

    def test_notification_is_deleted_when_user_is_deleted(self):
        self.basic_notification.user.delete()
        with self.assertRaises(ObjectDoesNotExist):
            self.basic_notification.refresh_from_db()
            self.assertFalse(Notification.objects.filter(id=self.basic_notification.id).exists())
        

    def test_notifying_user_can_be_blank(self):
        self.object_notification.notifying_user = None
        self._assert_object_notification_is_valid()

    def test_notification_is_deleted_when_notifying_user_is_deleted(self):
        self.object_notification.notifying_user.delete()
        with self.assertRaises(ObjectDoesNotExist):
            self.object_notification.refresh_from_db()
            self.assertFalse(Notification.objects.filter(id=self.object_notification.id).exists())


    def test_content_type_can_be_none(self):
        self.object_notification.content_type = None
        self._assert_object_notification_is_valid()

    def test_notification_is_deleted_when_content_type_is_deleted(self):
        self.object_notification.content_type.delete()
        with self.assertRaises(ObjectDoesNotExist):
            self.object_notification.refresh_from_db()
            self.assertFalse(Notification.objects.filter(id=self.object_notification.id).exists())


    def test_object_id_can_be_none(self):
        self.object_notification.object_id = None
        self._assert_object_notification_is_valid()


    def test_create_notification_with_no_content_object_has_default_fields(self):
        new_notification = Notification.objects.create(user=self.user)
        new_notification.full_clean()
        self.assertEqual(new_notification.title, "Default Title")
        self.assertEqual(new_notification.description, "Default description")
        self.assertEqual(new_notification.user, self.user)
        self.assertEqual(new_notification.notifying_user, None)
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, None)
        self.assertEqual(new_notification.object_id, None)
        self.assertEqual(new_notification.content_object, None)

    def test_create_notification_with_no_content_object_and_defined_fields(self):
        new_notification = Notification.objects.create(user=self.user, title="Test Title", description="Test description")
        new_notification.full_clean()
        self.assertEqual(new_notification.title, "Test Title")
        self.assertEqual(new_notification.description, "Test description")
        self.assertEqual(new_notification.user, self.user)
        self.assertEqual(new_notification.notifying_user, None)
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, None)
        self.assertEqual(new_notification.object_id, None)
        self.assertEqual(new_notification.content_object, None)


    def test_create_object_notification_with_friend_request(self):
        friend_request = FriendRequest.objects.get(id=1)
        new_notification = Notification.objects.create(user=friend_request.receiver, notifying_user=friend_request.sender, content_object=friend_request)
        new_notification.full_clean()
        self.assertEqual(new_notification.title, "New Friend Request")
        self.assertEqual(new_notification.description, "@johndoe has sent you a friend request.")
        self.assertEqual(new_notification.user, friend_request.receiver)
        self.assertEqual(new_notification.notifying_user, friend_request.sender)
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, ContentType.objects.get_for_model(FriendRequest))
        self.assertEqual(new_notification.object_id, friend_request.id)
        self.assertEqual(new_notification.content_object, friend_request)

    def test_create_object_notification_with_conversation(self):
        conversation = Conversation.objects.get(id=1)
        new_notification = Notification.objects.create(user=self.user, notifying_user=self.second_user, content_object=conversation)
        new_notification.full_clean()
        self.assertEqual(new_notification.title, "New Conversation")
        self.assertEqual(new_notification.description, "@janedoe has created a conversation with you.")
        self.assertEqual(new_notification.user, conversation.get_second_member())
        self.assertEqual(new_notification.notifying_user, conversation.get_first_member())
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, ContentType.objects.get_for_model(Conversation))
        self.assertEqual(new_notification.object_id, conversation.id)
        self.assertEqual(new_notification.content_object, conversation)

    def test_create_object_notification_with_group_conversation(self):
        conversation = Conversation.objects.get(id=2).as_group()
        new_notification = Notification.objects.create(user=self.user, notifying_user=self.second_user, content_object=conversation)
        new_notification.full_clean()
        self.assertEqual(new_notification.title, "New Group Conversation")
        self.assertEqual(new_notification.description, "@janedoe has added you to a group conversation.")
        self.assertEqual(new_notification.user, self.user)
        self.assertEqual(new_notification.notifying_user, self.second_user)
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, ContentType.objects.get_for_model(GroupConversation))
        self.assertEqual(new_notification.object_id, conversation.id)
        self.assertEqual(new_notification.content_object, conversation)

    def test_create_object_notification_with_post(self):
        post = Post.objects.get(id=1)
        liking_user = User.objects.get(id=2)
        new_notification = Notification.objects.create(user=post.author, notifying_user=liking_user, content_object=post, title="New Post Like")
        new_notification.full_clean()
        self.assertEqual(new_notification.title, "New Post Like")
        self.assertEqual(new_notification.description, "@janedoe has liked your post.")
        self.assertEqual(new_notification.user, post.author)
        self.assertEqual(new_notification.notifying_user, liking_user)
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, ContentType.objects.get_for_model(Post))
        self.assertEqual(new_notification.object_id, post.id)
        self.assertEqual(new_notification.content_object, post)

    def test_create_object_notification_with_post_comment(self):
        comment = PostComment.objects.get(id=1)
        post = Post.objects.get(id=1)
        new_notification = Notification.objects.create(user=post.author, notifying_user=comment.author, content_object=comment)
        new_notification.full_clean()
        self.assertEqual(new_notification.title, "New Post Comment")
        self.assertEqual(new_notification.description, "@johndoe has commented on your post.")
        self.assertEqual(new_notification.user, post.author)
        self.assertEqual(new_notification.notifying_user, comment.author)
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, ContentType.objects.get_for_model(PostComment))
        self.assertEqual(new_notification.object_id, comment.id)
        self.assertEqual(new_notification.content_object, comment)

    def test_create_object_notification_with_response(self):
        response = Response.objects.get(id=1)
        question = Question.objects.get(id=1)
        new_notification = Notification.objects.create(user=question.author, notifying_user=response.user, content_object=response)
        new_notification.full_clean()
        self.assertEqual(new_notification.title, "New Response")
        self.assertEqual(new_notification.description, "@johndoe has replied to your question.")
        self.assertEqual(new_notification.user, question.author)
        self.assertEqual(new_notification.notifying_user, response.user)
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, ContentType.objects.get_for_model(Response))
        self.assertEqual(new_notification.object_id, response.id)
        self.assertEqual(new_notification.content_object, response)

    def test_create_object_notification_with_other_content_object(self):
        content_user = User.objects.get(id=3)
        new_notification = Notification.objects.create(user=self.user, notifying_user=self.second_user, content_object=content_user)
        new_notification.full_clean()
        self.assertEqual(new_notification.title, "New User")
        self.assertEqual(new_notification.description, "Content type 'user' has no default description.")
        self.assertEqual(new_notification.user, self.user)
        self.assertEqual(new_notification.notifying_user, self.second_user)
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, ContentType.objects.get_for_model(User))
        self.assertEqual(new_notification.object_id, content_user.id)
        self.assertEqual(new_notification.content_object, content_user)

    def test_create_object_notification_with_other_content_object_no_notifying_user(self):
        content_user = User.objects.get(id=3)
        new_notification = Notification.objects.create(user=self.user, content_object=content_user)
        new_notification.full_clean()
        self.assertEqual(new_notification.title, "New User")
        self.assertEqual(new_notification.description, "Content type 'user' has no default description.")
        self.assertEqual(new_notification.user, self.user)
        self.assertEqual(new_notification.notifying_user, None)
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, ContentType.objects.get_for_model(User))
        self.assertEqual(new_notification.object_id, content_user.id)
        self.assertEqual(new_notification.content_object, content_user)


    def test_get_URL_for_notification_friend_request(self):
        friend_request = FriendRequest.objects.get(id=1)
        new_notification = Notification.objects.create(user=friend_request.receiver, notifying_user=friend_request.sender, content_object=friend_request)
        expected_url = reverse('profile', kwargs={'username': friend_request.sender})
        self.assertEqual(new_notification.get_URL(), expected_url)

    def test_get_URL_for_notification_conversation(self):
        conversation = Conversation.objects.get(id=1)
        new_notification = Notification.objects.create(user=self.user, notifying_user=self.second_user, content_object=conversation)
        expected_url = reverse('conversation', kwargs={'conversation_id': conversation.id})
        self.assertEqual(new_notification.get_URL(), expected_url)
        self.assertEqual(new_notification.get_conversation_URL(), expected_url)

    def test_get_URL_for_notification_group_conversation(self):
        conversation = Conversation.objects.get(id=2).as_group()
        new_notification = Notification.objects.create(user=self.user, notifying_user=self.second_user, content_object=conversation)
        expected_url = reverse('conversation', kwargs={'conversation_id': conversation.id})
        self.assertEqual(new_notification.get_URL(), expected_url)
        self.assertEqual(new_notification.get_conversation_URL(), expected_url)

    def test_get_URL_for_notification_post(self):
        post = Post.objects.get(id=1)
        liking_user = User.objects.get(id=2)
        new_notification = Notification.objects.create(user=post.author, notifying_user=liking_user, content_object=post)
        expected_url = reverse('post_detail', kwargs={'post_id': post.id})
        self.assertEqual(new_notification.get_URL(), expected_url)
        self.assertEqual(new_notification.get_post_URL(), expected_url)

    def test_get_URL_for_notification_post_comment(self):
        comment = PostComment.objects.get(id=1)
        post = Post.objects.get(id=1)
        new_notification = Notification.objects.create(user=post.author, notifying_user=comment.author, content_object=comment)
        expected_url = reverse('post_detail', kwargs={'post_id': post.id})
        self.assertEqual(new_notification.get_URL(), expected_url)
        self.assertEqual(new_notification.get_post_URL(), expected_url)

    def test_get_URL_for_notification_response(self):
        response = Response.objects.get(id=1)
        question = Question.objects.get(id=1)
        new_notification = Notification.objects.create(user=question.author, notifying_user=response.user, content_object=response)
        expected_url = reverse('question', kwargs={'id': question.id})
        self.assertEqual(new_notification.get_URL(), expected_url)
        self.assertEqual(new_notification.get_question_URL(), expected_url)

    def test_get_URL_for_notification_with_notifying_user_and_other_content_object(self):
        content_user = User.objects.get(id=3)
        new_notification = Notification.objects.create(user=self.user, notifying_user=self.second_user, content_object=content_user)
        expected_url = reverse('profile', kwargs={'username': new_notification.notifying_user})
        self.assertEqual(new_notification.get_URL(), expected_url)

    def test_get_URL_for_notification_with_other_content_object(self):
        content_user = User.objects.get(id=3)
        new_notification = Notification.objects.create(user=self.user, content_object=content_user)
        expected_url = reverse('inbox')
        self.assertEqual(new_notification.get_URL(), expected_url)

    def test_get_URL_for_notification_with_no_notifying_user_and_no_content_object(self):
        new_notification = Notification.objects.create(user=self.user, title="Test")
        expected_url = reverse('inbox')
        self.assertEqual(new_notification.get_URL(), expected_url)


    def test_get_is_friend_request(self):
        friend_request = FriendRequest.objects.get(id=1)
        new_notification = Notification.objects.create(user=friend_request.receiver, notifying_user=friend_request.sender, content_object=friend_request)
        self.assertTrue(new_notification.get_is_friend_request())

    def test_get_is_not_friend_request(self):
        conversation = Conversation.objects.get(id=1)
        new_notification = Notification.objects.create(user=conversation.get_first_member(), notifying_user=conversation.get_second_member(), content_object=conversation)
        self.assertFalse(new_notification.get_is_friend_request())

    def test_get_is_not_friend_request_for_no_content_type(self):
        new_notification = Notification.objects.create(user=self.user, notifying_user=self.second_user)
        self.assertFalse(new_notification.get_is_friend_request())

    
    def test_title_is_defined_in_save_if_no_title(self):
        friend_request = FriendRequest.objects.get(id=1)
        new_notification = Notification.objects.create(user=self.user, description="Test", notifying_user=self.second_user, content_object=friend_request)
        self.assertEqual(new_notification.title, "New Friend Request")

    def test_description_is_defined_in_save_if_no_description(self):
        friend_request = FriendRequest.objects.get(id=1)
        new_notification = Notification.objects.create(user=self.user, title="Test", notifying_user=self.second_user, content_object=friend_request)
        self.assertEqual(new_notification.description, "@janedoe has sent you a friend request.")
        


    def _assert_basic_notification_is_valid(self):
        self.basic_notification.full_clean()

    def _assert_basic_notification_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.basic_notification.full_clean()

    def _assert_object_notification_is_valid(self):
        self.object_notification.full_clean()

    def _assert_object_notification_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.object_notification.full_clean()