"""Unit tests of the parent form."""
import datetime
from django import forms
from django.test import TestCase
from peer_support.forms import UserForm, ParentForm
from peer_support.models import Parent

class ParentFormTestCase(TestCase):
    """Unit tests of the parent form."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_parent.json',
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
            'bio': 'I am a test patient.',
            'child_condition': 'Haemochromatosis',
            'child_age_of_diagnosis': 21,
        }

    def test_form_has_necessary_fields(self):
        form = ParentForm()
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
        self.assertIn('child_condition', form.fields)
        self.assertIn('child_age_of_diagnosis', form.fields)
        caod_widget = form.fields['child_age_of_diagnosis'].widget
        self.assertTrue(isinstance(caod_widget, forms.NumberInput))

    def test_parent_form_is_subclass_of_user_form(self):
        self.assertTrue(issubclass(ParentForm, UserForm))

    def test_valid_user_form(self):
        form = ParentForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'badusername'
        form = ParentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        user = Parent.objects.get(username='@johndoe')
        form = ParentForm(instance=user, data=self.form_input)
        before_count = Parent.objects.count()
        form.save()
        after_count = Parent.objects.count()
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
        self.assertEqual(user.bio, 'I am a test patient.'),
        self.assertEqual(user.child_condition, 'Haemochromatosis'),
        self.assertEqual(user.child_age_of_diagnosis, 21),
        self.assertEqual(before_count, after_count)
