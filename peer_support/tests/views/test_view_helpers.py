"""Unit tests for the helpers view."""
import uuid
from django.test import TestCase
from peer_support.models import Professional, Referral, User, Conversation, GroupConversation, Notification
from peer_support.views.helpers import create_referral, get_referral_code, get_addable_peers, check_blocked_dm, country_to_continent, country_to_continent_specific
from peer_support.views.helpers import filter_by_type, filter_by_timeframe
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse

class HelpersViewTestCase(TestCase):
    """Unit tests for the helpers view."""

    fixtures = [
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/other_professionals.json',
        'peer_support/tests/fixtures/default_conversation.json',
        'peer_support/tests/fixtures/default_message.json',
        'peer_support/tests/fixtures/other_messages.json',
        'peer_support/tests/fixtures/default_group_conversation.json',
        'peer_support/tests/fixtures/default_notification.json',
        'peer_support/tests/fixtures/other_notifications.json',
    ]

    def setUp(self):
        self.professional = Professional.objects.get(pk=12)
        self.user = User.objects.get(username='@johndoe') 

        
    def test_create_referral(self):
        referral = create_referral(self.professional)
        self.assertIsInstance(referral, Referral)
        self.assertEqual(referral.referrer, self.professional)
    
    def test_create_referral_invalid_user(self):
        invalid_user = 'invalid_user'
        referral = create_referral(invalid_user)
        self.assertIsNone(referral)

    def test_get_referral_code(self):
        code = uuid.uuid4().hex[:10].upper()
        Referral.objects.create(referrer=self.professional, code=code)
        referral_code = get_referral_code(self.professional)
        self.assertEqual(referral_code, code)

    def test_get_referral_code_no_referral(self):
        user = User.objects.get(id=1)
        referral_code = get_referral_code(user)
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
        self.assertIn(admin, addable_peers)
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

    def tearDown(self):
        Professional.objects.all().delete()
        Referral.objects.all().delete()
    
    def test_notification_is_created_within_past_24_hours(self):
        past_24_hours_notification = Notification.objects.create(created=timezone.now() - timedelta(hours=23), user=self.user)
        notifications = Notification.objects.all()
        notifications_within_past_24_hours = filter_by_timeframe(notifications, 'past_24_hours')
        self.assertIn(past_24_hours_notification, notifications_within_past_24_hours)

    def test_notification_is_not_created_within_past_24_hours(self):
        now = timezone.now()
        eariler_notification = Notification.objects.create(created=now - timedelta(hours=25), user=self.user)
        notifications = Notification.objects.all()
        notifications_within_past_24_hours = filter_by_timeframe(notifications, 'past_24_hours')
        self.assertNotIn(eariler_notification, notifications_within_past_24_hours)

    def test_notification_is_created_within_past_7_days(self):
        past_7_days_notification = Notification.objects.create(created=timezone.now() - timedelta(days=6), user=self.user)
        notifications = Notification.objects.all()
        notifications_within_past_7_days = filter_by_timeframe(notifications, 'past_7_days')
        self.assertIn(past_7_days_notification, notifications_within_past_7_days)

    def test_notification_is_created_within_past_4_weeks(self):
        past_4_weeks_notification = Notification.objects.create(created=timezone.now() - timedelta(weeks=3), user=self.user)
        notifications = Notification.objects.all()
        notifications_within_past_4_weeks = filter_by_timeframe(notifications, 'past_4_weeks')
        self.assertIn(past_4_weeks_notification, notifications_within_past_4_weeks)
        earlier_notifications = filter_by_timeframe(notifications, 'earlier')
        self.assertNotIn(past_4_weeks_notification, earlier_notifications)

    def test_earlier_notification_created_more_than_4_weeks_ago(self):
        earlier_notification = Notification.objects.create(created=timezone.now() - timedelta(weeks=5), user=self.user)
        past_4_weeks_notification = Notification.objects.create(created=timezone.now() - timedelta(weeks=3), user=self.user)
        notifications = Notification.objects.all()
        earlier_notifications = filter_by_timeframe(notifications, 'earlier')
        self.assertIn(earlier_notification, earlier_notifications)
        self.assertNotIn(past_4_weeks_notification, earlier_notifications)
    
    def test_notification_with_invalid_timeframe(self):
        notifications = Notification.objects.all()
        invalid_notification = Notification.objects.create(created=timezone.now() - timedelta(weeks=-9999), user=self.user)
        notifications_within_past_24_hours = filter_by_timeframe(notifications, 'past_24_hours')
        notifications_within_past_7_days = filter_by_timeframe(notifications, 'past_7_days')
        notifications_within_past_4_weeks = filter_by_timeframe(notifications, 'past_4_weeks')        
        earlier_notifications = filter_by_timeframe(notifications, 'earlier')
        self.assertNotIn(invalid_notification, notifications_within_past_24_hours)
        self.assertNotIn(invalid_notification, notifications_within_past_7_days)
        self.assertNotIn(invalid_notification, notifications_within_past_4_weeks)
        self.assertNotIn(invalid_notification, earlier_notifications)

    def test_notification_not_in_any_timeframe(self):
        notifications = Notification.objects.all()
        invalid_timeframe_notifications = filter_by_timeframe(notifications, 'invalid_timeframe')
        self.assertNotIn(notifications, invalid_timeframe_notifications)

    def test_filter_notification_by_content_type(self):
        post_comment_notification = Notification.objects.get(content_type_id=19)
        response_notification = Notification.objects.get(content_type_id=17)
        notifications = Notification.objects.all()
        
        post_comment_notifications = filter_by_type(notifications, 'post comment')
        response_notifications = filter_by_type(notifications, 'response')

        self.assertIn(post_comment_notification, post_comment_notifications)
        self.assertIn(response_notification, response_notifications)
        self.assertNotIn(response_notification, post_comment_notifications)
        self.assertIn(response_notification, notifications)

    def test_filter_by_type_other(self):
        other_notifications = filter_by_type(Notification.objects.all(), 'other')
        self.assertEqual(len(other_notifications), 1)
        for notification in other_notifications:
            self.assertIsNone(notification.content_type)