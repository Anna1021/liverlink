"""Unit tests of the user form."""
import datetime
from django import forms
from django.test import TestCase
from peer_support.forms import UserForm
from peer_support.models import User
from datetime import date, timedelta

class UserFormTestCase(TestCase):
    """Unit tests of the user form."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': '@janedoe',
            'email': 'janedoe@example.org',
            'date_of_birth': '1991-01-01',
            'gender': 'F',
            'location': 'US',
            'ethnicity': 'RO',
            'language': 'en',
            'bio': 'I am a test user.',
        }

    def test_form_has_necessary_fields(self):
        form = UserForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('date_of_birth', form.fields)
        dob_field = form.fields['date_of_birth']
        self.assertTrue(isinstance(dob_field, forms.DateField))
        dob_widget = dob_field.widget
        self.assertTrue(isinstance(dob_widget, forms.DateInput))
        self.assertIn('gender', form.fields)
        gender_widget = form.fields['gender'].widget
        self.assertTrue(isinstance(gender_widget, forms.Select))
        self.assertIn('location', form.fields)
        location_widget = form.fields['location'].widget
        self.assertTrue(isinstance(location_widget, forms.Select))
        self.assertIn('ethnicity', form.fields)
        ethnicity_widget = form.fields['ethnicity'].widget
        self.assertTrue(isinstance(ethnicity_widget, forms.Select))
        self.assertIn('language', form.fields)
        language_widget = form.fields['language'].widget
        self.assertTrue(isinstance(language_widget, forms.Select))
        self.assertIn('bio', form.fields)
        bio_widget = form.fields['bio'].widget
        self.assertTrue(isinstance(bio_widget, forms.Textarea))

    def test_valid_user_form(self):
        form = UserForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'badusername'
        form = UserForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        user = User.objects.get(username='@johndoe')
        form = UserForm(instance=user, data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(user.username, '@janedoe')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.org')
        self.assertEqual(user.date_of_birth, datetime.date(1991, 1, 1))
        self.assertEqual(user.gender, 'F')
        self.assertEqual(user.location, 'US')
        self.assertEqual(user.ethnicity, 'RO')
        self.assertEqual(user.language, 'en')
        self.assertEqual(user.bio, 'I am a test user.')
        self.assertEqual(before_count, after_count)

    def test_invalid_date_of_birth_less_than_13_years_ago(self):
        self.form_input['date_of_birth'] = date.today() - timedelta(days=365*12)
        form = UserForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['date_of_birth'], ['You must be 13 years old to register.'])
