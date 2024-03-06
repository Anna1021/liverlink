"""Unit tests of the sign up form."""
import datetime
from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from peer_support.forms import SignUpForm
from peer_support.models import Patient, Parent, Mentor, Referral
from django.core.exceptions import ValidationError

class SignUpFormTestCase(TestCase):
    """Unit tests of the sign up form."""
    
    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_mentor.json',
    ]

    def setUp(self):
        Referral.objects.create(referrer=Mentor.objects.get(username='@johndoe'), code='9C274FF391')

        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': '@janedoe',
            'email': 'janedoe@example.org',
            'date_of_birth': '2004-03-02',
            'gender': 'F',
            'location': 'GB',
            'hospital': 'Croydon Health Services NHS Trust',
            'ethnicity': 'RO',
            'language': 'en',
            'bio': 'I am a test user.',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
            'user_type': 'PT',
            'condition': 'Cancer',
            'transplant': 'N',
            'age_of_diagnosis': 5,
        }

    def test_valid_sign_up_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('date_of_birth', form.fields)
        date_of_birth_field = form.fields['date_of_birth']
        self.assertTrue(isinstance(date_of_birth_field, forms.DateField))
        self.assertIn('gender', form.fields)
        self.assertIn('location', form.fields)
        self.assertIn('hospital', form.fields)
        self.assertIn('ethnicity', form.fields)
        self.assertIn('language', form.fields)
        self.assertIn('bio', form.fields)
        bio_field = form.fields['bio']
        self.assertTrue(isinstance(bio_field, forms.CharField))
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))
        self.assertIn('user_type', form.fields)
        self.assertIn('condition', form.fields)
        self.assertIn('transplant', form.fields)
        self.assertIn('age_of_diagnosis', form.fields)

    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'badusername'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = 'PasswordABC'
        self.form_input['password_confirmation'] = 'PasswordABC'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_are_identical(self):
        self.form_input['password_confirmation'] = 'WrongPassword123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly_with_patient(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        before_count = Patient.objects.count()
        form.save()
        after_count = Patient.objects.count()
        self.assertEqual(after_count, before_count+1)
        user = Patient.objects.get(username='@janedoe')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.org')
        self.assertEqual(user.date_of_birth, datetime.date(2004, 3, 2))
        self.assertEqual(user.gender, 'F')
        self.assertEqual(user.location, 'GB')
        self.assertEqual(user.hospital, 'Croydon Health Services NHS Trust')
        self.assertEqual(user.ethnicity, 'RO')
        self.assertEqual(user.language, 'en')
        self.assertEqual(user.bio, 'I am a test user.')
        self.assertEqual(user.condition, 'Cancer')
        self.assertEqual(user.transplant, 'N')
        self.assertEqual(user.age_of_diagnosis, 5)
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)

    def test_form_must_save_correctly_with_parent(self):
        self.form_input['user_type'] = 'PR'
        self.form_input['child_condition'] = 'Cancer'
        self.form_input['child_transplant'] = 'N'
        self.form_input['child_age_of_diagnosis'] = 5
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        before_count = Parent.objects.count()
        form.save()
        after_count = Parent.objects.count()
        self.assertEqual(after_count, before_count+1)
        user = Parent.objects.get(username='@janedoe')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.org')
        self.assertEqual(user.date_of_birth, datetime.date(2004, 3, 2))
        self.assertEqual(user.gender, 'F')
        self.assertEqual(user.location, 'GB')
        self.assertEqual(user.hospital, 'Croydon Health Services NHS Trust')
        self.assertEqual(user.ethnicity, 'RO')
        self.assertEqual(user.language, 'en')
        self.assertEqual(user.bio, 'I am a test user.')
        self.assertEqual(user.child_condition, 'Cancer')
        self.assertEqual(user.child_transplant, 'N')
        self.assertEqual(user.child_age_of_diagnosis, 5)
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)

    def test_mentor_referal_validation(self):
        self.form_input['user_type'] = 'MT'
        self.form_input['condition'] = 'Cancer'
        self.form_input['transplant'] = 'N'
        self.form_input['age_of_diagnosis'] = 5
        self.form_input['referral_code']='NONEXISTING'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly_with_mentor(self):
        self.form_input['user_type'] = 'MT'
        self.form_input['condition'] = 'Cancer'
        self.form_input['transplant'] = 'N'
        self.form_input['age_of_diagnosis'] = 5
        self.form_input['referral_code']='9C274FF391'
        form = SignUpForm(data=self.form_input)
        before_count = Mentor.objects.count()
        self.assertTrue(form.is_valid())
        form.save()
        after_count = Mentor.objects.count()
        self.assertEqual(after_count, before_count+1)
        user = Mentor.objects.get(username='@janedoe')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.org')
        self.assertEqual(user.date_of_birth, datetime.date(2004, 3, 2))
        self.assertEqual(user.gender, 'F')
        self.assertEqual(user.location, 'GB')
        self.assertEqual(user.hospital, 'Croydon Health Services NHS Trust')
        self.assertEqual(user.ethnicity, 'RO')
        self.assertEqual(user.language, 'en')
        self.assertEqual(user.bio, 'I am a test user.')
        self.assertEqual(user.condition, 'Cancer')
        self.assertEqual(user.transplant, 'N')
        self.assertEqual(user.age_of_diagnosis, 5)
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)

    def test_invalid_referral_code(self):
        self.form_input['referral_code']='INVALID_CODE'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_clean_method_invalid_referral_code(self):
        self.form_input['referral_code']='INVALID_CODE'
        form = SignUpForm(data=self.form_input)
        form.full_clean()
        self.assertFalse(form.is_valid())

    def test_clean_method_invalid_user_type(self):
        self.form_input['user_type']='PT '
        form = SignUpForm(data=self.form_input)
        form.full_clean()
        self.assertFalse(form.is_valid())