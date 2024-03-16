"""Unit test of search peer form"""
from django.test import TestCase
from peer_support.forms import SearchUserForm
from peer_support.models import User

class SearchUserFormTestCase(TestCase):
    """Unit test of search peer form"""
    
    fixtures = [
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
    ]

    def setUp(self):
        self.users = User.objects.all()

    def test_form_initialization(self):
        form = SearchUserForm()
        self.assertFalse(form.is_bound)
        self.assertIn('search', form.fields)

    def test_search(self):
        form_data = {'search': 'Jane'}
        form = SearchUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        search_results = form.search_users(self.users)
        self.assertTrue(search_results.exists())
        self.assertIn(User.objects.get(username='@janedoe'), search_results)
        self.assertNotIn(User.objects.get(username='@petrapickles'), search_results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), search_results)

    def test_search_no_results(self):
        form_data = {'search': 'NonexistentUser'}
        form = SearchUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        search_results = form.search_users(self.users)
        self.assertFalse(search_results.exists())

    def test_search_blank(self):
        form_data = {'search': ''}
        form = SearchUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        search_results = form.search_users(self.users)
        self.assertEqual(search_results.count(), self.users.count())
    
    def test_search_name(self):
        form_data = {'search': 'rsi'}
        form = SearchUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        search_results = form.search_users(self.users)
        self.assertTrue(search_results.exists())
        self.assertIn(User.objects.get(username='@mohamedalf'), search_results)
        self.assertNotIn(User.objects.get(username='@petrapickles'), search_results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), search_results)