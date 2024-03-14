"""Unit tests for the User model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from peer_support.models import User

class UserModelTestCase(TestCase):
    """Unit tests for the User model."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
    ]

    GRAVATAR_URL = "https://www.gravatar.com/avatar/363c1b0cd64dadffb867236a00e62986"

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_can_be_30_characters_long(self):
        self.user.username = '@' + 'x' * 29
        self._assert_user_is_valid()

    def test_username_cannot_be_over_30_characters_long(self):
        self.user.username = '@' + 'x' * 30
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.username = second_user.username
        self._assert_user_is_invalid()

    def test_username_must_start_with_at_symbol(self):
        self.user.username = 'johndoe'
        self._assert_user_is_invalid()

    def test_username_must_contain_only_alphanumericals_after_at(self):
        self.user.username = '@john!doe'
        self._assert_user_is_invalid()

    def test_username_must_contain_at_least_3_alphanumericals_after_at(self):
        self.user.username = '@jo'
        self._assert_user_is_invalid()

    def test_username_may_contain_numbers(self):
        self.user.username = '@j0hndoe2'
        self._assert_user_is_valid()

    def test_username_must_contain_only_one_at(self):
        self.user.username = '@@johndoe'
        self._assert_user_is_invalid()


    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_first_name_may_contain_50_characters(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_must_not_contain_more_than_50_characters(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid()


    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_last_name_may_contain_50_characters(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_must_not_contain_more_than_50_characters(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid()


    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.email = second_user.email
        self._assert_user_is_invalid()

    def test_email_must_contain_username(self):
        self.user.email = '@example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = 'johndoe.example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = 'johndoe@.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user.email = 'johndoe@example'
        self._assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email = 'johndoe@@example.org'
        self._assert_user_is_invalid()



    def test_date_of_birth_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.date_of_birth = second_user.date_of_birth
        self._assert_user_is_valid()

    def test_date_of_birth_must_not_be_blank(self):
        self.user.date_of_birth = None
        self._assert_user_is_invalid()

    def test_date_of_birth_must_be_13_years_ago(self):
        self.user.date_of_birth = '2008-01-01'
        self._assert_user_is_valid()


    def test_gender_may_be_blank(self):
        self.user.gender = None
        self._assert_user_is_valid()

    def test_gender_can_only_be_one_of_the_choices(self):
        self.user.gender = "Alien"
        self._assert_user_is_invalid()

    def gender_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.gender = second_user.gender
        self._assert_user_is_valid()


    def test_location_may_be_blank(self):
        self.user.location = None
        self._assert_user_is_valid()

    def test_location_can_only_be_one_of_the_choices(self):
        self.user.location = 'Mars'
        self._assert_user_is_invalid()

    def test_location_must_not_contain_more_than_50_characters(self):
        self.user.location = 'x' * 51
        self._assert_user_is_invalid()

    def test_location_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.location = second_user.location
        self._assert_user_is_valid()


    def test_hospital_may_be_blank(self):
        self.user.hospital = None
        self._assert_user_is_valid()

    def test_hospital_can_only_be_one_of_the_choices(self):
        self.user.hospital = 'Mars General'
        self._assert_user_is_invalid()

    def test_hospital_must_not_contain_more_than_500_characters(self):
        self.user.hospital = 'x' * 501
        self._assert_user_is_invalid()

    def test_hospital_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.hospital = second_user.hospital
        self._assert_user_is_valid()

    
    def test_ethnicity_may_be_blank(self):
        self.user.ethnicity = None
        self._assert_user_is_valid()

    def test_ethnicity_can_only_be_one_of_the_choices(self):
        self.user.ethnicity = 'Martian'
        self._assert_user_is_invalid()

    def test_ethnicity_must_not_contain_more_than_50_characters(self):
        self.user.ethnicity = 'x' * 51
        self._assert_user_is_invalid()

    def test_ethnicity_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.ethnicity = second_user.ethnicity
        self._assert_user_is_valid()


    def test_language_may_be_blank(self):
        self.user.language = None
        self._assert_user_is_valid()

    def test_language_can_only_be_one_of_the_choices(self):
        self.user.language = 'Martian'
        self._assert_user_is_invalid()

    def test_language_must_not_contain_more_than_50_characters(self):
        self.user.language = 'x' * 51
        self._assert_user_is_invalid()

    def test_language_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.language = second_user.language
        self._assert_user_is_valid()


    def test_bio_may_be_blank(self):
        self.user.bio = ''
        self._assert_user_is_valid()

    def test_bio_may_contain_500_characters(self):
        self.user.bio = 'x' * 500
        self._assert_user_is_valid()

    def test_bio_must_not_contain_more_than_500_characters(self):
        self.user.bio = 'x' * 501
        self._assert_user_is_invalid()

    def test_bio_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.bio = second_user.bio
        self._assert_user_is_valid()

    
    def test_friends_may_be_blank(self):
        self.user.friends.clear()
        self._assert_user_is_valid()

    
    def test_conversations_may_be_blank(self):
        self.user.conversations.clear()
        self._assert_user_is_valid()


    def test_first_login_defaults_to_true(self):
        self.assertTrue(self.user.first_login)

    
    def test_full_name_must_be_correct(self):
        full_name = self.user.full_name()
        self.assertEqual(full_name, "John Doe")


    def test_country_name_must_be_correct(self):
        country_name = self.user.country_name()
        self.assertEqual(country_name, "United Kingdom")

    def test_country_name_can_be_blank(self):
        self.user.location = None
        country_name = self.user.country_name()
        self.assertEqual(country_name, "")


    def test_gender_name_must_be_correct(self):
        gender_name = self.user.gender_name()
        self.assertEqual(gender_name, "Male")


    def test_gender_name_can_be_blank(self):
        self.user.gender = None
        gender_name = self.user.gender_name()
        self.assertEqual(gender_name, "")

    
    def test_ethnicity_name_must_be_correct(self):
        ethnicity_name = self.user.ethnicity_name()
        self.assertEqual(ethnicity_name, "English, Welsh, Scottish, Northern Irish or British")

    def test_ethnicity_name_can_be_blank(self):
        self.user.ethnicity = None
        ethnicity_name = self.user.ethnicity_name()
        self.assertEqual(ethnicity_name, "")

    def test_unknown_ethnicity_name(self):
        self.user.ethnicity = "Unknown"
        ethnicity_name = self.user.ethnicity_name()
        self.assertEqual(ethnicity_name, "")

    
    def test_language_name_must_be_correct(self):
        language_name = self.user.language_name()
        self.assertEqual(language_name, "English")

    def test_language_name_can_be_blank(self):
        self.user.language = None
        language_name = self.user.language_name()
        self.assertEqual(language_name, "")


    def test_default_gravatar(self):
        actual_gravatar_url = self.user.gravatar()
        expected_gravatar_url = self._gravatar_url(size=120)
        self.assertEqual(actual_gravatar_url, expected_gravatar_url)

    def test_custom_gravatar(self):
        actual_gravatar_url = self.user.gravatar(size=100)
        expected_gravatar_url = self._gravatar_url(size=100)
        self.assertEqual(actual_gravatar_url, expected_gravatar_url)

    def test_mini_gravatar(self):
        actual_gravatar_url = self.user.mini_gravatar()
        expected_gravatar_url = self._gravatar_url(size=60)
        self.assertEqual(actual_gravatar_url, expected_gravatar_url)

    def _gravatar_url(self, size):
        gravatar_url = f"{UserModelTestCase.GRAVATAR_URL}?size={size}&default=mp"
        return gravatar_url


    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()