import uuid
from django.test import TestCase
from peer_support.models import Mentor, Referral, User
from peer_support.views.helpers import create_referral, get_referral_code, get_addable_peers

class HelpersViewTestCase(TestCase):
    """Unit tests for the helpers view."""

    fixtures = [
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
    ]

    def setUp(self):
        self.mentor = Mentor.objects.create(username='test_mentor')
        
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
        addable_peers = get_addable_peers(current_user)
        self.assertNotIn(current_user, addable_peers)
        self.assertNotIn(admin, addable_peers)
        self.assertNotIn(friend, addable_peers)

    def tearDown(self):
        Mentor.objects.all().delete()
        Referral.objects.all().delete()