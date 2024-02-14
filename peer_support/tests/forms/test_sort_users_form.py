"""Unit test of SortPeerForm"""
from django.test import TestCase
from peer_support.forms import SortPeerForm 
from django.test import TestCase
from peer_support.models import User,Patient,Parent
from datetime import date

class SortPeerFormTestCase(TestCase):
    """Unit test of SortPeerForm"""

    def setUp(self):
        today = date.today()
        self.current_user = Patient.objects.create(
            username="@janedoe",
            email="janedoe@example.com",
            date_of_birth=date(today.year - 30, today.month, today.day),
            gender="F",
            location="GB",
            hospital="Guy’s and St Thomas’ NHS Foundation Trust",
            ethnicity="OM",
            language="en",
            condition="Biliary atresia",
            age_of_diagnosis=2
        )    
        Patient.objects.create(
            username="@peterpickles",
            email="peterpickles@example.com",
            date_of_birth=date(today.year - 25, today.month, today.day),
            gender="F",
            location="GB",
            hospital="Airedale NHS Foundation Trust",
            ethnicity="BD",
            language="en",
            condition="Biliary atresia",
            age_of_diagnosis=2
        )
        Parent.objects.create(
            username="@petrapickles",
            email="petrapickles@example.com",
            date_of_birth=date(today.year - 20, today.month, today.day),
            gender="F",
            location="GB",
            hospital="Airedale NHS Foundation Trust",
            ethnicity="BD",
            language="en",
            child_condition="Biliary atresia",
            child_age_of_diagnosis=5
        )
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
        sorted_users = form.sort_users(self.users, self.current_user)
        self.assertEqual(sorted_users[0].username, "@janedoe")
        self.assertEqual(sorted_users[1].username, "@peterpickles")
        self.assertEqual(sorted_users[2].username, "@petrapickles")

    def test_sort_users_by_username_descending(self):
        form_data = {'sort_by': 'username_desc'}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user)
        self.assertEqual(sorted_users[0].username, "@petrapickles")
        self.assertEqual(sorted_users[1].username, "@peterpickles")
        self.assertEqual(sorted_users[2].username, "@janedoe")

    def test_sort_users_by_age_ascending(self):
        form_data = {'sort_by': 'age_asc'}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user)
        self.assertEqual(sorted_users[0].username, "@petrapickles")
        self.assertEqual(sorted_users[1].username, "@peterpickles")
        self.assertEqual(sorted_users[2].username, "@janedoe")

    def test_sort_users_by_age_descending(self):
        form_data = {'sort_by': 'age_desc'}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user)
        self.assertEqual(sorted_users[0].username, "@janedoe")
        self.assertEqual(sorted_users[1].username, "@peterpickles")
        self.assertEqual(sorted_users[2].username, "@petrapickles")
    
    def test_sort_users_by_best_match(self):
        form_data = {'sort_by': ''}
        form = SortPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user)
        expected_order = ['@janedoe', '@peterpickles', '@petrapickles']
        sorted_usernames = [user.username for user in sorted_users]
        self.assertEqual(sorted_usernames, expected_order)
        