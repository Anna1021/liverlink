"""Unit test of SearchPeerForm """
from django.test import TestCase
from peer_support.forms import SearchPeerForm
from peer_support.models import User

class SearchPeerFormTestCase(TestCase):
    """Unit test of SearchPeerForm """
    fixtures = [
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
    ]

    def setUp(self):
        self.users = User.objects.all()

    def test_form_initialization(self):
        form = SearchPeerForm()
        self.assertFalse(form.is_bound)
        self.assertIn('search', form.fields)

    def test_search(self):
        form_data = {'search': 'Jane'}
        form = SearchPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        search_results = form.search_users(self.users)
        self.assertTrue(search_results.exists())
        self.assertIn(User.objects.get(username='@janedoe'), search_results)

        self.assertNotIn(User.objects.get(username='@petrapickles'), search_results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), search_results)

    def test_search_no_results(self):
        form_data = {'search': 'NonexistentUser'}
        form = SearchPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        search_results = form.search_users(self.users)
        self.assertFalse(search_results.exists())

    def test_search_blank(self):
        form_data = {'search': ''}
        form = SearchPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        search_results = form.search_users(self.users)
        self.assertEqual(search_results.count(), self.users.count())