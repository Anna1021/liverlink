"""Unit tests for the UserProfile model."""
import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from peer_support.models import User, Patient, Parent, UserProfile

class UserProfileModelTestCase(TestCase):
    """Unit tests for the UserProfile model."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_user_profile.json',
        'peer_support/tests/fixtures/other_user_profiles.json',
    ]

    def setUp(self):
        self.user_profile = UserProfile.objects.get(id=1)

    def test_valid_user_profile(self):
        self._assert_user_profile_is_valid()

    
    def test_user_profile_is_automatically_created_when_new_user_is_created(self):
        before_count = UserProfile.objects.count()
        User.objects.create_user(username="@tester", 
                                 first_name="test", 
                                 last_name="account", 
                                 email="test@test.org",
                                 password="Password123",
                                 date_of_birth=datetime.date(1990,1,1),
                                 gender="M",
                                 location="GB",
                                 ethnicity="BR",
                                 language="en",
                                 bio="abc")
        after_count = UserProfile.objects.count()
        self.assertEqual(before_count+1, after_count)
        new_user = User.objects.get(username="@tester")
        user_profile = UserProfile.objects.get(user=new_user)
        self.assertEqual(new_user, user_profile.user) # New user is the same user assigned to new user profile
        self.assertEqual(new_user.id, user_profile.id) # New user ID is the same as new user profile ID

    def test_user_profile_is_automatically_created_when_new_patient_is_created(self):
        # ! Does not work - check against latest merge
        before_count = UserProfile.objects.count()
        Patient.objects.create_user(username="@tester", 
                                    first_name="test", 
                                    last_name="account", 
                                    email="test@test.org",
                                    password="Password123",
                                    date_of_birth=datetime.date(1990,1,1),
                                    gender="M",
                                    location="GB",
                                    ethnicity="BR",
                                    language="en",
                                    bio="abc",
                                    condition="Hepatitis",
                                    age_of_diagnosis=20)
        after_count = UserProfile.objects.count()
        self.assertEqual(before_count+1, after_count)
        new_patient = Patient.objects.get(username="@tester")
        user_profile = UserProfile.objects.get(user=new_patient)
        self.assertEqual(new_patient, user_profile.user) # New patient is the same user assigned to new user profile
        self.assertEqual(new_patient.id, user_profile.id) # New patient ID is the same as new user profile ID

    def test_user_profile_is_automatically_created_when_new_parent_is_created(self):
        # ! Does not work - check against latest merge
        before_count = UserProfile.objects.count()
        Parent.objects.create_user(username="@tester", 
                                    first_name="test", 
                                    last_name="account", 
                                    email="test@test.org",
                                    password="Password123",
                                    date_of_birth=datetime.date(1990,1,1),
                                    gender="M",
                                    location="GB",
                                    ethnicity="BR",
                                    language="en",
                                    bio="abc",
                                    child_condition="Hepatitis",
                                    child_age_of_diagnosis=20)
        after_count = UserProfile.objects.count()
        self.assertEqual(before_count+1, after_count)
        new_parent = Parent.objects.get(username="@tester")
        user_profile = UserProfile.objects.get(user=new_parent)
        self.assertEqual(new_parent, user_profile.user) # New parent is the same user assigned to new user profile
        self.assertEqual(new_parent.id, user_profile.id) # New parent ID is the same as new user profile ID


    def test_user_cannot_be_none(self):
        self.user_profile.user = None
        self._assert_user_profile_is_invalid()

    def test_user_profile_is_deleted_when_associated_user_is_deleted(self):
        self.user_profile.user.delete()
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(id=self.user_profile.id)
    
    def test_user_must_be_unique(self):
        second_user = UserProfile.objects.get(id=2).user
        self.user_profile.user = second_user
        self._assert_user_profile_is_invalid()


    def test_theme_cannot_be_blank(self):
        self.user_profile.theme = ''
        self._assert_user_profile_is_invalid()

    def test_theme_need_not_be_unique(self):
        second_theme = UserProfile.objects.get(id=2).theme
        self.user_profile.theme = second_theme
        self._assert_user_profile_is_valid()
    
    def test_theme_can_be_within_given_choices(self):
        for choice in UserProfile.THEME_CHOICES:
            self.user_profile.theme = choice[0]
            self._assert_user_profile_is_valid()

    def test_theme_cannot_be_outside_of_given_choices(self):
        self.user_profile.theme = "TESTING"
        self._assert_user_profile_is_invalid()

    
    def test_font_cannot_be_blank(self):
        self.user_profile.font = ''
        self._assert_user_profile_is_invalid()

    def test_font_need_not_be_unique(self):
        second_font = UserProfile.objects.get(id=2).font
        self.user_profile.font = second_font
        self._assert_user_profile_is_valid()
    
    def test_font_can_be_within_given_choices(self):
        for choice in UserProfile.FONT_CHOICES:
            self.user_profile.font = choice[0]
            self._assert_user_profile_is_valid()

    def test_font_cannot_be_outside_of_given_choices(self):
        self.user_profile.font = "TESTING"
        self._assert_user_profile_is_invalid()

    
    def test_font_size_cannot_be_blank(self):
        self.user_profile.font_size = ''
        self._assert_user_profile_is_invalid()

    def test_font_size_need_not_be_unique(self):
        second_font_size = UserProfile.objects.get(id=2).font_size
        self.user_profile.font_size = second_font_size
        self._assert_user_profile_is_valid()
    
    def test_font_size_can_be_within_given_choices(self):
        for choice in UserProfile.FONT_SIZE_CHOICES:
            self.user_profile.font_size = choice[0]
            self._assert_user_profile_is_valid()

    def test_font_size_cannot_be_outside_of_given_choices(self):
        self.user_profile.font_size = "TESTING"
        self._assert_user_profile_is_invalid()

    
    def test_friends_can_be_empty(self):
        self.user_profile.friends.clear()
        self._assert_user_profile_is_valid()


    def test_blocked_users_can_be_empty(self):
        self.user_profile.blocked_users.clear()
        self._assert_user_profile_is_valid()

    
    def _assert_user_profile_is_valid(self):
        try:
            self.user_profile.full_clean()
        except (ValidationError):
            self.fail('Test user profile should be valid')

    def _assert_user_profile_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user_profile.full_clean()