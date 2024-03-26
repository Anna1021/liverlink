"""Unit tests for the UserProfile model."""
import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from peer_support.models import User, Patient, Parent, Mentor, Professional, UserProfile

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
        self.assertEqual(new_user, user_profile.user)
        self.assertEqual(new_user.id, user_profile.id)

    def test_user_profile_is_automatically_created_when_new_patient_is_created(self):
        before_count = UserProfile.objects.count()
        Patient.objects.create(username="@tester", 
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
                                    transplant="N",
                                    age_of_diagnosis=20)
        after_count = UserProfile.objects.count()
        self.assertEqual(before_count+1, after_count)
        new_patient = Patient.objects.get(username="@tester")
        new_patient_user = User.objects.get(username="@tester")
        user_profile = UserProfile.objects.get(user=new_patient)
        self.assertEqual(new_patient_user, user_profile.user)
        self.assertEqual(new_patient.id, user_profile.id)

    def test_user_profile_is_automatically_created_when_new_parent_is_created(self):
        before_count = UserProfile.objects.count()
        Parent.objects.create(username="@tester", 
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
                                    child_transplant="N",
                                    child_age_of_diagnosis=20)
        after_count = UserProfile.objects.count()
        self.assertEqual(before_count+1, after_count)
        new_parent = Parent.objects.get(username="@tester")
        new_parent_user = User.objects.get(username="@tester")
        user_profile = UserProfile.objects.get(user=new_parent)
        self.assertEqual(new_parent_user, user_profile.user)
        self.assertEqual(new_parent.id, user_profile.id)

    def test_user_profile_is_automatically_created_when_new_mentor_is_created(self):
        before_count = UserProfile.objects.count()
        Mentor.objects.create(username="@tester", 
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
                                    transplant="N",
                                    age_of_diagnosis=20,
                                    referral_code='TEST123')
        after_count = UserProfile.objects.count()
        self.assertEqual(before_count+1, after_count)
        new_mentor = Mentor.objects.get(username="@tester")
        new_mentor_user = User.objects.get(username="@tester")
        user_profile = UserProfile.objects.get(user=new_mentor)
        self.assertEqual(new_mentor_user, user_profile.user)
        self.assertEqual(new_mentor.id, user_profile.id)

    def test_user_profile_is_automatically_created_when_new_professional_is_created(self):
        before_count = UserProfile.objects.count()
        Professional.objects.create(username="@tester", 
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
                                    expertise="Hepatitis",
                                    referral_code='TEST123')
        after_count = UserProfile.objects.count()
        self.assertEqual(before_count+1, after_count)
        new_professional = Professional.objects.get(username="@tester")
        new_professional_user = User.objects.get(username="@tester")
        user_profile = UserProfile.objects.get(user=new_professional)
        self.assertEqual(new_professional_user, user_profile.user)
        self.assertEqual(new_professional.id, user_profile.id)


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

    
    def test_profile_picture_can_be_blank(self):
        self.user_profile.profile_picture = ''
        self._assert_user_profile_is_valid()

    def test_profile_picture_need_not_be_unique(self):
        second_profile_picture = UserProfile.objects.get(id=2).profile_picture
        self.user_profile.profile_picture = second_profile_picture
        self._assert_user_profile_is_valid()
        
    
    def _assert_user_profile_is_valid(self):
        try:
            self.user_profile.full_clean()
        except (ValidationError):
            self.fail('Test user profile should be valid')

    def _assert_user_profile_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user_profile.full_clean()