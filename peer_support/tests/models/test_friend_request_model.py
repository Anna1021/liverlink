"""Unit tests for the FriendRequest model."""
from django.test import TestCase
from django.core.exceptions import ValidationError
from peer_support.models import User, FriendRequest

class FriendRequestModelTestCase(TestCase):
    """Unit tests for the FriendRequest model."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_friend_request.json',
        'peer_support/tests/fixtures/other_friend_requests.json'
    ]

    def setUp(self):
        self.sender = User.objects.get(username='@johndoe')
        self.receiver = User.objects.get(username='@janedoe')
        self.friend_request = FriendRequest.objects.get(sender=self.sender, receiver=self.receiver)

    def test_valid_friend_request(self):
        self._assert_friend_request_is_valid()

    def test_sender_cannot_be_blank(self):
        self.friend_request.sender = None
        self._assert_friend_request_is_invalid()

    def test_receiver_cannot_be_blank(self):
        self.friend_request.receiver = None
        self._assert_friend_request_is_invalid()

    def test_is_accepted_defaults_to_false(self):
        self.assertFalse(self.friend_request.is_accepted)

    def _assert_friend_request_is_valid(self):
        self.friend_request.full_clean()

    def _assert_friend_request_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.friend_request.full_clean()