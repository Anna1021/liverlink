"""Unit test of SortPeerForm"""
from django.test import TestCase
from peer_support.forms import SortPeerForm 
from django.test import TestCase
from peer_support.models import User,Patient,Parent
from datetime import date

class SortPeerFormTestCase(TestCase):
    """Unit test of SortPeerForm"""

    fixtures = [
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/other_parents.json',
    ]

    def setUp(self):
        self.current_user_patient = Patient.objects.get(username='@janedoe')
        self.current_user_parent =  Parent.objects.get(username='@mohamedalf')
        self.username_asc_order= ['@alexsmith', '@janedoe', '@mohamedalf','@peterpickles','@petrapickles','@sambennet']
        self.age_asc_order=['@janedoe', '@petrapickles',  '@alexsmith','@mohamedalf','@peterpickles']
        self.users = User.objects.all()

    def test_form_has_necessary_fields(self):
        form = SortPeerForm()
        self.assertIn('sort_by', form.fields)

    def test_form_accepts_valid_input(self):
        form_data = {'sort_by': 'username_asc'}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_sort_users_by_username_ascending(self):
        form_data = {'sort_by': 'username_asc'}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user_patient)
        expected_order = self.username_asc_order
        sorted_usernames = [user.username for user in sorted_users]
        self.assertEqual(sorted_usernames, expected_order)

    def test_sort_users_by_username_descending(self):
        form_data = {'sort_by': 'username_desc'}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user_patient)
        expected_order = self.username_asc_order[::-1]
        sorted_usernames = [user.username for user in sorted_users]
        self.assertEqual(sorted_usernames, expected_order)

    def test_sort_users_by_age_ascending(self):
        form_data = {'sort_by': 'age_asc'}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user_patient)
        expected_order = self.age_asc_order+['@sambennet']
        sorted_usernames = [user.username for user in sorted_users]
        self.assertEqual(sorted_usernames, expected_order)

    def test_sort_users_by_age_descending(self):
        form_data = {'sort_by': 'age_desc'}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user_patient)
        expected_order = self.age_asc_order[::-1]+['@sambennet']
        sorted_usernames = [user.username for user in sorted_users]
        self.assertEqual(sorted_usernames, expected_order)
        
    def test_sort_users_by_best_match_patient(self):
        form_data = {'sort_by': ''}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user_patient)
        expected_order = ['@janedoe', '@petrapickles', '@peterpickles', '@sambennet','@mohamedalf','@alexsmith']
        sorted_usernames = [user.username for user in sorted_users]
        self.assertEqual(sorted_usernames, expected_order)

    def test_sort_users_by_best_match_parent(self):
        form_data = {'sort_by': ''}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user_parent)        
        expected_order = ['@mohamedalf','@alexsmith', '@sambennet','@peterpickles','@janedoe','@petrapickles']
        sorted_usernames = [user.username for user in sorted_users]
        self.assertEqual(sorted_usernames, expected_order)   

    def test_invalid_user_form(self):
        form_data = {'sort_by': ''}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, None)
        self.assertGreater(len(sorted_users), 0, "The sorted users list should not be empty.")
