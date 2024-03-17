"""Tests of the friends list view."""
from django.test import TestCase
from django.urls import reverse
from peer_support.tests.helpers import reverse_with_next
from peer_support.models import User
from django.utils.http import urlencode
from peer_support.forms import FilterUserForm, SortUserForm, SearchUserForm

class FriendsListViewTestCase(TestCase):
    """Tests of the friends list view."""
    
    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',]
    
    def setUp(self):
        self.url = reverse('friends_list')
        self.user = User.objects.get(username='@petrapickles')
        self.client.force_login(self.user)

    def test_friends_list_url(self):
        self.assertEqual(self.url, '/friends_list/')
        
    def test_friends_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'friends_list.html')
        self.assertEqual(len(response.context['friends']), 2)
        self.assertEqual(response.context['friends'][0]['friend'], User.objects.get(username='@peterpickles'))
        self.assertEqual(response.context['friends'][0]['user_type'], 'ADMIN')
        self.assertIsInstance(response.context['form_sort'], SortUserForm)
        self.assertIsInstance(response.context['form_filter'], FilterUserForm)
        self.assertIsInstance(response.context['form_search'], SearchUserForm)

    def test_friends_list_without_being_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_profile_redirects_when_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_form_filter_functionality(self):
        filter_params = {'gender': ['N']}  
        response = self.client.get(self.url, filter_params)
        self.assertEqual(response.status_code, 200)
        filtered_friends = list(response.context['friends'])
        for user_dict in filtered_friends:
            self.assertEqual(user_dict['friend'].gender, 'N')

    def test_form_sort_functionality(self):
        sort_data = {'sort_by': 'username_asc'}
        response = self.client.get(self.url, sort_data)
        self.assertEqual(response.status_code, 200)
        sorted_friends = response.context['friends']
        sorted_usernames = [user_dict['friend'].username for user_dict in sorted_friends]
        manual_sorted_friends = sorted(sorted_friends, key=lambda x: x['friend'].username)
        manual_sorted_usernames = [user_dict['friend'].username for user_dict in manual_sorted_friends]
        self.assertEqual(sorted_usernames, manual_sorted_usernames)

    def test_search_functionality(self):
        sort_params = {'search': 'peter'}
        response = self.client.get(f"{self.url}?{urlencode(sort_params)}")
        self.assertEqual(response.status_code, 200)    
        search_friends = response.context['friends']
        self.assertTrue(any(user_dict['friend'].username == '@peterpickles' for user_dict in search_friends))
        self.assertEqual(len(search_friends), 1, "Should only find one user matching 'jane'")

    def test_invalid_filter_form_submission(self):
        invalid_filter_params = {'gender': 'InvalidGender', 'language': 'xx'}
        response = self.client.get(self.url, invalid_filter_params)
        self.assertFalse(response.context['form_filter'].is_valid())

    def test_invalid_sort_form_submission(self):
        invalid_sort_params = {'sort_by': 'InvalidSort'} 
        response = self.client.get(self.url, invalid_sort_params)
        self.assertFalse(response.context['form_sort'].is_valid(), "Form was expected to be invalid but was valid")

    def test_search_max_length_exceeded(self):
        search_term = 'a' * 256  
        invalid_sort_params = {'search': search_term}
        response = self.client.get(self.url, invalid_sort_params)
        self.assertFalse(response.context['form_search'].is_valid())
    
