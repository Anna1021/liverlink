import uuid
import datetime
from django.test import TestCase
from peer_support.models import Mentor, Referral, User, Conversation, GroupConversation
from peer_support.views.helpers import create_referral, get_referral_code, get_addable_peers, check_blocked_dm, user_exists

class HelpersViewTestCase(TestCase):
    """Unit tests for the helpers view."""

    fixtures = [
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
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

    def tearDown(self):
        Mentor.objects.all().delete()
        Referral.objects.all().delete()

    def test_user_exists(self):
        self.assertTrue(user_exists('@petrapickles'))
