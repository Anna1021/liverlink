"""Tests for the post template tags"""
from django.test import TestCase
from peer_support.templatetags.post_tags import likes_summary
from peer_support.models import User

class PostTagsTestCase(TestCase):
    """Tests for the post template tags"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.users = User.objects.all()

    def test_less_than_10_likes(self):
        users = [self.user]
        summary = likes_summary(users)
        expected_summary = str(self.user)
        self.assertEqual(summary, expected_summary)

    def test_more_than_or_equal_10_likes(self):
        summary = likes_summary(self.users)
        expected_summary = ', '.join(str(user) for user in self.users[:10]) + ' +{} more'.format(len(self.users) - 10)
        self.assertEqual(summary, expected_summary)