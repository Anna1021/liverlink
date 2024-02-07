from django.test import TestCase
from peer_support.forms import SortPeerForm 
from django.test import TestCase
from peer_support.models import User

class SortPeerFormTestCase(TestCase):
    """Test for sort form of users"""

    fixtures = [
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json'
    ]

    def setUp(self):
        self.users = User.objects.all().order_by('id') 

    def test_form_has_necessary_fields(self):
        form = SortPeerForm()
        self.assertIn('Username', form.fields)
        self.assertIn('Age', form.fields)

    def test_form_accepts_valid_input(self):
        form_data = {'Username': 'asc'}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_rejects_both_criteria_selected(self):
        form_data = {'Username': 'asc', 'Age': 'desc'}
        form = SortPeerForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_sort_users_by_username_ascending(self):
        form_data = {'Username': 'asc'}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users)
        self.assertEqual(sorted_users[0].username, "@janedoe")
        self.assertEqual(sorted_users[1].username, "@peterpickles")
        self.assertEqual(sorted_users[2].username, "@petrapickles")

    def test_sort_users_by_username_descending(self):
        form_data = {'Username': 'desc'}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users)
        self.assertEqual(sorted_users[0].username, "@petrapickles")
        self.assertEqual(sorted_users[1].username, "@peterpickles")
        self.assertEqual(sorted_users[2].username, "@janedoe")

    def test_sort_users_by_age_ascending(self):
        form_data = {'Age': 'asc'}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users)
        self.assertEqual(sorted_users[0].username, "@peterpickles")
        self.assertEqual(sorted_users[1].username, "@petrapickles")
        self.assertEqual(sorted_users[2].username, "@janedoe")

    def test_sort_users_by_age_descending(self):
        form_data = {'Age': 'desc'}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users)
        self.assertEqual(sorted_users[0].username, "@janedoe")
        self.assertEqual(sorted_users[1].username, "@petrapickles")
        self.assertEqual(sorted_users[2].username, "@peterpickles")