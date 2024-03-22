"""Unit tests for the helpers view."""
import uuid
import datetime
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from peer_support.models import Mentor, Referral, User, Conversation, GroupConversation, Notification, FriendRequest, Response, PostComment
from peer_support.views.helpers import create_referral, get_referral_code, get_addable_peers, check_blocked_dm, send_notification, send_notification_to_parent, country_to_continent, country_to_continent_specific

class HelpersViewTestCase(TestCase):
    """Unit tests for the helpers view."""

    fixtures = [
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/default_friend_request.json',
        'peer_support/tests/fixtures/default_conversation.json',
        'peer_support/tests/fixtures/default_message.json',
        'peer_support/tests/fixtures/other_messages.json',
        'peer_support/tests/fixtures/default_group_conversation.json',
        'peer_support/tests/fixtures/default_question.json',
        'peer_support/tests/fixtures/default_response.json',
        'peer_support/tests/fixtures/default_post.json',
        'peer_support/tests/fixtures/default_post_comment.json',
    ]

    def setUp(self):
        self.mentor = Mentor.objects.create(username='@test_mentor', date_of_birth=datetime.date(1990,1,1),)
        
    def test_create_referral(self):
        referral = create_referral(self.mentor)
        self.assertIsInstance(referral, Referral)
        self.assertEqual(referral.referrer, self.mentor)
    
    def test_create_referral_invalid_user(self):
        invalid_user = 'invalid_user'
        referral = create_referral(invalid_user)
        self.assertIsNone(referral)

    def test_get_referral_code(self):
        code = uuid.uuid4().hex[:10].upper()
        Referral.objects.create(referrer=self.mentor, code=code)
        referral_code = get_referral_code(self.mentor)
        self.assertEqual(referral_code, code)

    def test_get_referral_code_no_referral(self):
        referral_code = get_referral_code(self.mentor)
        self.assertIsNone(referral_code)

    def test_country_to_continent_known(self):
        self.assertEqual(country_to_continent('US'), 'North America')

    def test_country_to_continent_unknown(self):
        self.assertEqual(country_to_continent('XX'), 'Unknown') 

    def test_country_to_continent_two_known(self):
        self.assertEqual(country_to_continent_specific('US'), ('North America', 'United States'))

    def test_country_to_continent_two_unknown(self):
        self.assertEqual(country_to_continent_specific('XX'), ('Unknown', 'Unknown'))
    
    def test_get_addable_peers(self):
        current_user = User.objects.get(username='@petrapickles')
        admin = User.objects.get(username='@admin')
        friend = User.objects.get(username='@peterpickles')
        blocked_user = User.objects.get(username='@alexsmith')
        current_user.blocked_users.add(blocked_user)
        blocked_by_user = User.objects.get(username='@sambennet')
        blocked_by_user.blocked_users.add(current_user)
        addable_peers = get_addable_peers(current_user)
        self.assertNotIn(current_user, addable_peers)
        self.assertNotIn(admin, addable_peers)
        self.assertNotIn(friend, addable_peers)
        self.assertNotIn(blocked_user, addable_peers)
        self.assertNotIn(blocked_by_user, addable_peers)

    def test_check_blocked_dm_on_direct_conversation_users_not_blocked(self):
        user = User.objects.get(username='@janedoe')
        second_user = User.objects.get(username='@petrapickles')
        direct_conversation = Conversation.objects.create()
        direct_conversation.users.add(user)
        direct_conversation.users.add(second_user)
        self.assertIsNone(direct_conversation.as_group())
        self.assertFalse(check_blocked_dm(user, direct_conversation))
        self.assertFalse(check_blocked_dm(second_user, direct_conversation))

    def test_check_blocked_dm_on_direct_conversation_users_blocked(self):
        user = User.objects.get(username='@janedoe')
        second_user = User.objects.get(username='@petrapickles')
        user.blocked_users.add(second_user)
        direct_conversation = Conversation.objects.create()
        direct_conversation.users.add(user)
        direct_conversation.users.add(second_user)
        self.assertIsNone(direct_conversation.as_group())
        self.assertTrue(check_blocked_dm(user, direct_conversation))
        self.assertTrue(check_blocked_dm(second_user, direct_conversation))

    def test_check_blocked_dm_on_group_conversation(self):
        user = User.objects.get(username='@janedoe')
        second_user = User.objects.get(username='@petrapickles')
        third_user = User.objects.get(username='@peterpickles')
        group_conversation = GroupConversation.objects.create()
        group_conversation.users.add(user)
        group_conversation.users.add(second_user)
        group_conversation.users.add(third_user)
        self.assertIsNotNone(group_conversation.as_group())
        self.assertFalse(check_blocked_dm(user, group_conversation))
        self.assertFalse(check_blocked_dm(second_user, group_conversation))

    def test_send_notification_for_friend_request(self):
        friend_request = FriendRequest.objects.get(id=1)
        before_count = Notification.objects.count()
        send_notification(friend_request)
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 1, after_count)
        new_notification = Notification.objects.last()
        self.assertEqual(new_notification.title, "New Friend Request")
        self.assertEqual(new_notification.description, f"{friend_request.sender} has sent you a friend request.")
        self.assertEqual(new_notification.user, friend_request.receiver)
        self.assertEqual(new_notification.notifying_user, friend_request.sender)
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, ContentType.objects.get_for_model(FriendRequest))
        self.assertEqual(new_notification.object_id, friend_request.id)
        self.assertEqual(new_notification.content_object, friend_request)

    def test_send_notification_for_conversation(self):
        conversation = Conversation.objects.get(id=1)
        before_count = Notification.objects.count()
        send_notification(conversation, conv_user=conversation.get_first_member(), conv_creator=conversation.get_second_member())
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 1, after_count)
        new_notification = Notification.objects.last()
        self.assertEqual(new_notification.title, "New Conversation")
        self.assertEqual(new_notification.description, f"{conversation.get_second_member()} has created a conversation with you.")
        self.assertEqual(new_notification.user, conversation.get_first_member())
        self.assertEqual(new_notification.notifying_user, conversation.get_second_member())
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, ContentType.objects.get_for_model(Conversation))
        self.assertEqual(new_notification.object_id, conversation.id)
        self.assertEqual(new_notification.content_object, conversation)

    def test_send_notification_for_conversation_with_no_kwargs_does_not_create_notification(self):
        conversation = Conversation.objects.get(id=1)
        before_count = Notification.objects.count()
        send_notification(conversation)
        after_count = Notification.objects.count()
        self.assertEqual(before_count, after_count)
        content_type_id = ContentType.objects.get_for_model(Conversation)
        self.assertFalse(Notification.objects.filter(content_type=content_type_id, object_id=conversation.id).exists())

    def test_send_notification_for_conversation_with_missing_conv_user_kwarg_does_not_create_notification(self):
        conversation = Conversation.objects.get(id=1)
        before_count = Notification.objects.count()
        send_notification(conversation, conv_creator=conversation.get_first_member())
        after_count = Notification.objects.count()
        self.assertEqual(before_count, after_count)
        content_type_id = ContentType.objects.get_for_model(Conversation)
        self.assertFalse(Notification.objects.filter(content_type=content_type_id, object_id=conversation.id).exists())

    def test_send_notification_for_conversation_with_missing_conv_creator_kwarg_does_not_create_notification(self):
        conversation = Conversation.objects.get(id=1)
        before_count = Notification.objects.count()
        send_notification(conversation, conv_user=conversation.get_first_member())
        after_count = Notification.objects.count()
        self.assertEqual(before_count, after_count)
        content_type_id = ContentType.objects.get_for_model(Conversation)
        self.assertFalse(Notification.objects.filter(content_type=content_type_id, object_id=conversation.id).exists())

    def test_send_notification_for_group_conversation(self):
        conversation = Conversation.objects.get(id=2).as_group()
        before_count = Notification.objects.count()
        first_user = conversation.users.all()[0]
        second_user = conversation.users.all()[1]
        send_notification(conversation, conv_user=first_user, conv_creator=second_user)
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 1, after_count)
        new_notification = Notification.objects.last()
        self.assertEqual(new_notification.title, "New Group Conversation")
        self.assertEqual(new_notification.description, f"{conversation.get_second_member()} has added you to a group conversation.")
        self.assertEqual(new_notification.user, first_user)
        self.assertEqual(new_notification.notifying_user, second_user)
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, ContentType.objects.get_for_model(GroupConversation))
        self.assertEqual(new_notification.object_id, conversation.id)
        self.assertEqual(new_notification.content_object, conversation)

    def test_send_notification_for_response(self):
        response = Response.objects.get(id=1)
        response.user = User.objects.get(id=2)
        before_count = Notification.objects.count()
        send_notification(response)
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 1, after_count)
        new_notification = Notification.objects.last()
        self.assertEqual(new_notification.title, "New Response")
        self.assertEqual(new_notification.description, f"{response.user} has replied to your question.")
        self.assertEqual(new_notification.user, response.question.author)
        self.assertEqual(new_notification.notifying_user, response.user)
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, ContentType.objects.get_for_model(Response))
        self.assertEqual(new_notification.object_id, response.id)
        self.assertEqual(new_notification.content_object, response)

    def test_send_two_notification_for_response_with_parent(self):
        parent_response = Response.objects.get(id=1)
        child_response = Response.objects.create(user=User.objects.get(id=2),
                                                question=parent_response.question,
                                                parent=parent_response,
                                                body='This is a child response.')
        self.assertIsNotNone(child_response.parent)
        before_count = Notification.objects.count()
        send_notification(child_response)
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 2, after_count)
        content_type_id = ContentType.objects.get_for_model(Response)
        self.assertTrue(Notification.objects.filter(content_type=content_type_id, object_id=child_response.id).count(), 2)

    def test_send_notification_for_response_to_own_question_does_not_create_notification(self):
        response = Response.objects.get(id=1)
        self.assertEqual(response.question.author, response.user)
        before_count = Notification.objects.count()
        send_notification(response)
        after_count = Notification.objects.count()
        self.assertEqual(before_count, after_count)
        content_type_id = ContentType.objects.get_for_model(Response)
        self.assertFalse(Notification.objects.filter(content_type=content_type_id, object_id=response.id).exists())

    def test_send_notification_for_post_comment(self):
        comment = PostComment.objects.get(id=1)
        comment.author = User.objects.get(id=2)
        before_count = Notification.objects.count()
        send_notification(comment)
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 1, after_count)
        new_notification = Notification.objects.last()
        self.assertEqual(new_notification.title, "New Post Comment")
        self.assertEqual(new_notification.description, f"{comment.author} has commented on your post.")
        self.assertEqual(new_notification.user, comment.post.author)
        self.assertEqual(new_notification.notifying_user, comment.author)
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, ContentType.objects.get_for_model(PostComment))
        self.assertEqual(new_notification.object_id, comment.id)
        self.assertEqual(new_notification.content_object, comment)

    def test_send_notification_for_post_comment_with_parent(self):
        parent_comment = PostComment.objects.get(id=1)
        child_comment = PostComment.objects.create(author=User.objects.get(id=2),
                                                post=parent_comment.post,
                                                parent=parent_comment,
                                                content='This is a child comment.')
        self.assertIsNotNone(child_comment.parent)
        before_count = Notification.objects.count()
        send_notification(child_comment)
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 2, after_count)
        content_type_id = ContentType.objects.get_for_model(PostComment)
        self.assertTrue(Notification.objects.filter(content_type=content_type_id, object_id=child_comment.id).count(), 2)

    def test_send_notification_for_post_comment_on_own_post_does_not_create_notification(self):
        comment = PostComment.objects.get(id=1)
        self.assertEqual(comment.post.author, comment.author)
        before_count = Notification.objects.count()
        send_notification(comment)
        after_count = Notification.objects.count()
        self.assertEqual(before_count, after_count)
        content_type_id = ContentType.objects.get_for_model(PostComment)
        self.assertFalse(Notification.objects.filter(content_type=content_type_id, object_id=comment.id).exists())

    def test_send_notification_for_other_content_object_does_not_create_notification(self):
        user = User.objects.get(id=1)
        before_count = Notification.objects.count()
        send_notification(user)
        after_count = Notification.objects.count()
        self.assertEqual(before_count, after_count)
        content_type_id = ContentType.objects.get_for_model(User)
        self.assertFalse(Notification.objects.filter(content_type=content_type_id, object_id=user.id).exists())

    def test_send_parent_notification_for_response(self):
        parent_response = Response.objects.get(id=1)
        child_response = Response.objects.create(user=User.objects.get(id=2),
                                                question=parent_response.question,
                                                parent=parent_response,
                                                body='This is a child response.')
        self.assertIsNotNone(child_response.parent)
        before_count = Notification.objects.count()
        send_notification_to_parent(child_response, child_response.user)
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 1, after_count)
        new_notification = Notification.objects.last()
        self.assertEqual(new_notification.title, "New Response")
        self.assertEqual(new_notification.description, f"{child_response.user} has replied to your reply.")
        self.assertEqual(new_notification.user, parent_response.user)
        self.assertEqual(new_notification.notifying_user, child_response.user)
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, ContentType.objects.get_for_model(Response))
        self.assertEqual(new_notification.object_id, child_response.id)
        self.assertEqual(new_notification.content_object, child_response)

    def test_send_parent_notification_for_response_without_parent_does_not_create_notification(self):
        response = Response.objects.get(id=1)
        self.assertIsNone(response.parent)
        before_count = Notification.objects.count()
        send_notification(response)
        after_count = Notification.objects.count()
        self.assertEqual(before_count, after_count)
        content_type_id = ContentType.objects.get_for_model(Response)
        self.assertFalse(Notification.objects.filter(content_type=content_type_id, object_id=response.id).exists())

    def test_send_parent_notification_for_response_by_same_author_as_parent_does_not_create_notification(self):
        parent_response = Response.objects.get(id=1)
        child_response = Response.objects.create(user=User.objects.get(id=2),
                                                question=parent_response.question,
                                                parent=parent_response,
                                                body='This is a child response.')
        child_response.user = parent_response.user
        before_count = Notification.objects.count()
        send_notification(child_response)
        after_count = Notification.objects.count()
        self.assertEqual(before_count, after_count)
        content_type_id = ContentType.objects.get_for_model(Response)
        self.assertFalse(Notification.objects.filter(content_type=content_type_id, object_id=child_response.id).exists())

    def test_send_parent_notification_for_post_comment(self):
        parent_comment = PostComment.objects.get(id=1)
        child_comment = PostComment.objects.create(author=User.objects.get(id=2),
                                                post=parent_comment.post,
                                                parent=parent_comment,
                                                content='This is a child comment.')
        self.assertIsNotNone(child_comment.parent)
        before_count = Notification.objects.count()
        send_notification_to_parent(child_comment, child_comment.author)
        after_count = Notification.objects.count()
        self.assertEqual(before_count + 1, after_count)
        new_notification = Notification.objects.last()
        self.assertEqual(new_notification.title, "New Post Comment")
        self.assertEqual(new_notification.description, f"{child_comment.author} has replied to your reply.")
        self.assertEqual(new_notification.user, parent_comment.author)
        self.assertEqual(new_notification.notifying_user, child_comment.author)
        self.assertEqual(new_notification.viewed, False)
        self.assertEqual(new_notification.content_type, ContentType.objects.get_for_model(PostComment))
        self.assertEqual(new_notification.object_id, child_comment.id)
        self.assertEqual(new_notification.content_object, child_comment)

    def test_send_parent_notification_for_post_comment_without_parent_does_not_create_notification(self):
        comment = PostComment.objects.get(id=1)
        self.assertIsNone(comment.parent)
        before_count = Notification.objects.count()
        send_notification(comment)
        after_count = Notification.objects.count()
        self.assertEqual(before_count, after_count)
        content_type_id = ContentType.objects.get_for_model(PostComment)
        self.assertFalse(Notification.objects.filter(content_type=content_type_id, object_id=comment.id).exists())

    def test_send_parent_notification_for_post_comment_by_same_author_as_parent_does_not_create_notification(self):
        parent_comment = PostComment.objects.get(id=1)
        child_comment = PostComment.objects.create(author=User.objects.get(id=2),
                                                post=parent_comment.post,
                                                parent=parent_comment,
                                                content='This is a child comment.')
        child_comment.author = parent_comment.author
        before_count = Notification.objects.count()
        send_notification(child_comment)
        after_count = Notification.objects.count()
        self.assertEqual(before_count, after_count)
        content_type_id = ContentType.objects.get_for_model(PostComment)
        self.assertFalse(Notification.objects.filter(content_type=content_type_id, object_id=child_comment.id).exists())

    def tearDown(self):
        Mentor.objects.all().delete()
        Referral.objects.all().delete()