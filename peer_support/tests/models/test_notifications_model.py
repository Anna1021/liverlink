"""Unit tests for the Notification model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from peer_support.models import User, Notification

class NotificationModelTestCase(TestCase):
    """Unit tests for the Notification model."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_notification.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.notification = Notification.objects.get(user=self.user)

    def test_valid_notification(self):
        self._assert_notification_is_valid()

    def test_title_cannot_be_blank(self):
        self.notification.title = ''
        self._assert_notification_is_invalid()

    def test_title_can_be_100_characters_long(self):
        self.notification.title = 'x' * 100
        self._assert_notification_is_valid()

    def test_title_cannot_be_over_100_characters_long(self):
        self.notification.title = 'x' * 101
        self._assert_notification_is_invalid()


    def test_description_can_be_blank(self):
        self.notification.description = ''
        self._assert_notification_is_valid()

    def test_description_can_be_1000_characters_long(self):
        self.notification.description = 'x' * 1000
        self._assert_notification_is_valid()

    def test_description_cannot_be_over_1000_characters_long(self):
        self.notification.description = 'x' * 1001
        self._assert_notification_is_invalid()


    def test_created_defaults_to_now(self):
        self.notification.save()
        self.assertIsNotNone(self.notification.created)


    def test_viewed_defaults_to_false(self):
        self.assertFalse(self.notification.viewed)


    def test_user_cannot_be_blank(self):
        self.notification.user = None
        self._assert_notification_is_invalid()
        

    def test_friend_request_can_be_blank(self):
        self.notification.friend_request = None
        self._assert_notification_is_valid()
        

    def _assert_notification_is_valid(self):
        self.notification.full_clean()

    def _assert_notification_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.notification.full_clean()