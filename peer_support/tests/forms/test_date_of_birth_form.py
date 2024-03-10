from datetime import date, timedelta
from django.test import TestCase
from peer_support.models import User
from peer_support.forms import SignUpForm

class DateOfBirthTestCase(TestCase):

    fixtures = ['peer_support/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {
            'date_of_birth': "2004-07-08",
        }

    def test_valid_date_of_birth(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_invalid_date_of_birth_less_than_13_years_ago(self):
        self.form_input['date_of_birth'] = date.today() - timedelta(days=365*12)
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['date_of_birth'], ['You must be 13 years old to register.'])

