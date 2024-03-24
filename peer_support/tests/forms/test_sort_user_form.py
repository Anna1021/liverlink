"""Unit test of sort peer form"""
import datetime
from django.test import TestCase
from peer_support.forms import SortUserForm 
from peer_support.models import User, Patient, Parent, Mentor, Professional

class SortUserFormTestCase(TestCase):
    """Unit test of sort peer form"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_mentor.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/other_parents.json',
        'peer_support/tests/fixtures/other_professionals.json',
    ]

    def setUp(self):
        self.current_user_patient = Patient.objects.get(username='@janedoe')
        self.current_user_parent =  Parent.objects.get(username='@mohamedalf')
        self.current_user_professional = Professional.objects.get(username= '@annamiller')
        self.current_user_mentor =  Mentor.objects.get(username='@johndoe')
        self.username_asc_order= ['@alexsmith', '@annamiller', '@carlosmartinez', '@craighughes','@hazelsmith', '@janedoe', '@johndoe', '@lindajohnson', '@mohamedalf', '@peterpickles', '@petrapickles', '@rajpatel', '@sambennet']
        self.age_asc_order=['@janedoe', '@craighughes', '@johndoe', '@petrapickles', '@sambennet', '@rajpatel', '@lindajohnson', '@hazelsmith', '@alexsmith', '@annamiller', '@carlosmartinez', '@mohamedalf', '@peterpickles']
        self.users = User.objects.all()

    def test_form_has_necessary_fields(self):
        form = SortUserForm()
        self.assertIn('sort_by', form.fields)

    def test_form_accepts_valid_input(self):
        form_data = {'sort_by': 'username_asc'}
        form = SortUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_sort_users_by_username_ascending(self):
        form_data = {'sort_by': 'username_asc'}
        form = SortUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user_patient)
        expected_order = self.username_asc_order
        sorted_usernames = [user.username for user in sorted_users]
        self.assertEqual(sorted_usernames, expected_order)

    def test_sort_users_by_username_descending(self):
        form_data = {'sort_by': 'username_desc'}
        form = SortUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user_patient)
        expected_order = self.username_asc_order[::-1]
        sorted_usernames = [user.username for user in sorted_users]
        self.assertEqual(sorted_usernames, expected_order)

    def test_sort_users_by_age_ascending(self):
        form_data = {'sort_by': 'age_asc'}
        form = SortUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user_patient)
        expected_order = self.age_asc_order
        sorted_usernames = [user.username for user in sorted_users]
        self.assertEqual(sorted_usernames, expected_order)

    def test_sort_users_by_age_descending(self):
        form_data = {'sort_by': 'age_desc'}
        form = SortUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user_patient)
        expected_order = self.age_asc_order[::-1]
        sorted_usernames = [user.username for user in sorted_users]
        self.assertEqual(sorted_usernames, expected_order)
        
    def test_sort_users_by_best_match_patient(self):
        form_data = {'sort_by': ''}
        form = SortUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user_patient)
        expected_order = ['@janedoe','@johndoe', '@petrapickles', '@peterpickles', '@sambennet', '@craighughes','@lindajohnson','@annamiller','@hazelsmith','@mohamedalf','@carlosmartinez', '@rajpatel','@alexsmith']
        sorted_usernames = [user.username for user in sorted_users]
        self.assertEqual(sorted_usernames, expected_order)

    def test_sort_users_by_best_match_parent(self):
        form_data = {'sort_by': ''}
        form = SortUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user_parent)        
        expected_order = ['@mohamedalf','@alexsmith', '@sambennet', '@craighughes','@carlosmartinez', '@rajpatel', '@lindajohnson', '@annamiller', '@hazelsmith','@peterpickles','@johndoe' ,'@janedoe','@petrapickles']
        sorted_usernames = [user.username for user in sorted_users]
        self.assertEqual(sorted_usernames, expected_order)   

    def test_invalid_user_form(self):
        form_data = {'sort_by': ''}
        form = SortUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, None)
        self.assertGreater(len(sorted_users), 0, "The sorted users list should not be empty.")
   
    def test_empty_user_sort_without_errors(self):
        new_user = User.objects.create_user(
            username="@newuser",
            email="newuser@example.com",
            date_of_birth=datetime.date(1990,1,1),
            first_name="New",
            last_name="User",
            password="testpassword123")
        form_data = {'sort_by': ''}
        form = SortUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        users = User.objects.all()
        sorted_users = form.sort_users(users, new_user)
        self.assertTrue(sorted_users, "Sorted users should not be empty.")
       
    def test_empty_user_sort_without_errors_patient(self):
        new_user = Patient.objects.create_user(
            username="@newuser",
            email="newuser@example.com",
            date_of_birth=datetime.date(1990,1,1),
            first_name="New",
            last_name="User",
            password="testpassword123"
            )
        form_data = {'sort_by': ''}
        form = SortUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        users = User.objects.all()
        sorted_users = form.sort_users(users, new_user)
        self.assertTrue(sorted_users, "Sorted users should not be empty.")

    def test_empty_user_sort_without_errors_parent(self):
        new_user = Parent.objects.create_user(
            username="@newuser",
            email="newuser@example.com",
            date_of_birth=datetime.date(1990,1,1),
            first_name="New",
            last_name="User",
            password="testpassword123"
            )
        form_data = {'sort_by': ''}
        form = SortUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        users = User.objects.all()
        sorted_users = form.sort_users(users, new_user)
        self.assertTrue(sorted_users, "Sorted users should not be empty.")

    def test_empty_user_sort_without_errors_mentor(self):
        new_user = Mentor.objects.create_user(
            username="@newuser",
            email="newuser@example.com",
            date_of_birth=datetime.date(1990,1,1),
            first_name="New",
            last_name="User",
            password="testpassword123"
            )
        form_data = {'sort_by': ''}
        form = SortUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        users = User.objects.all()
        sorted_users = form.sort_users(users, new_user)
        self.assertTrue(sorted_users, "Sorted users should not be empty.")
    
    def test_sort_users_by_best_match_mentor(self):
        form_data = {'sort_by': ''}
        form = SortUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user_mentor)
        expected_order = ['@johndoe', '@petrapickles','@janedoe', '@peterpickles', '@sambennet','@craighughes', '@rajpatel', '@mohamedalf', '@carlosmartinez', '@alexsmith', '@lindajohnson', '@annamiller', '@hazelsmith']
        sorted_usernames = [user.username for user in sorted_users]
        self.assertEqual(sorted_usernames, expected_order)   
    
    def test_sort_users_by_best_match_professional(self):
        form_data = {'sort_by': ''}
        form = SortUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        sorted_users = form.sort_users(self.users, self.current_user_professional)
        expected_order = ['@peterpickles','@annamiller', '@craighughes','@rajpatel', '@alexsmith', '@hazelsmith','@sambennet','@lindajohnson', '@mohamedalf', '@carlosmartinez','@janedoe','@petrapickles','@johndoe']
        sorted_usernames = [user.username for user in sorted_users]
        self.assertEqual(sorted_usernames, expected_order)   
    
