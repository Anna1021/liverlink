from django.test import TestCase
from django.urls import reverse
from peer_support.forms import FilterPeerForm, SortPeerForm, SearchPeerForm
from peer_support.models import User
from peer_support.tests.helpers import reverse_with_next
from django.utils.http import urlencode

class PeerSelectViewTestCase(TestCase):
    """Tests of the Peer Select view."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_parent.json',
        'peer_support/tests/fixtures/default_admin.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
    ]

    def setUp(self):
        self.url = reverse('peer_select')
        self.user = User.objects.get(username='@johndoe')
        self.client.force_login(self.user)

    def test_peer_select_url(self):
        self.assertEqual(self.url,'/peer_select/')

    def test_get_peer_select(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'peer_select.html')
        self.assertIsInstance(response.context['formSort'], SortPeerForm)
        self.assertIsInstance(response.context['formFilter'], FilterPeerForm)
        self.assertIsInstance(response.context['formSearch'], SearchPeerForm)

    def test_all_forms_shown(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="gender"') 
        self.assertContains(response, 'name="language"')
        self.assertContains(response, 'name="sort_by"')
        self.assertContains(response, 'name="search"')

    def test_get_profile_redirects_when_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_form_filter_functionality(self):
        filter_params = {'gender': ['F'], 'language': 'en'}  
        response = self.client.get(self.url, filter_params)
        self.assertEqual(response.status_code, 200)
        filtered_users = list(response.context['users'])
        for user in filtered_users:
            self.assertEqual(user.gender, 'F')
            self.assertTrue(user.language, 'en')

    def test_form_sort_functionality(self):
        sort_data = {'sort_by': 'username_asc'}
        response = self.client.get(self.url, sort_data)
        self.assertEqual(response.status_code, 200)
        sorted_users = response.context['users']
        sorted_usernames = [user.username for user in sorted_users]
        manual_sorted_users = sorted_users.order_by('username')
        manual_sorted_usernames = [user.username for user in manual_sorted_users]
        self.assertEqual(sorted_usernames,manual_sorted_usernames)

    def test_search_functionality(self):
        sort_params = {'search': 'jane'}
        response = self.client.get(f"{self.url}?{urlencode(sort_params)}")
        self.assertEqual(response.status_code, 200)    
        search_users = response.context['users']
        self.assertTrue(any(user.username == '@janedoe' for user in search_users))
        self.assertEqual(len(search_users), 1, "Should only find one user matching 'jane'")

    def test_invalid_filter_form_submission(self):
        invalid_filter_params = {'gender': 'InvalidGender', 'language': 'xx'}
        response = self.client.get(self.url, invalid_filter_params)
        self.assertFalse(response.context['formFilter'].is_valid())

    def test_invalid_sort_form_submission(self):
        invalid_sort_params = {'sort_by': 'InvalidSort'} 
        response = self.client.get(self.url, invalid_sort_params)
        self.assertFalse(response.context['formSort'].is_valid(), "Form was expected to be invalid but was valid")

    def test_search_max_length_exceeded(self):
        search_term = 'a' * 256  
        invalid_sort_params = {'search': search_term}
        response = self.client.get(self.url, invalid_sort_params)
        self.assertFalse(response.context['formSearch'].is_valid())
    
    def test_exclude_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        users = response.context['users']
        self.assertNotIn(self.user, users)

    def test_exclude_admin(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        users = response.context['users']
        for user in users:
            self.assertFalse(user.is_staff or user.is_superuser, "Admin users should not be included in the list.")

    def test_exclude_friends(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        users = response.context['users']
        for user in users:
            self.assertNotIn(user, self.user.friends.all())

    def test_exclude_blocked_users(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.blocked_users.add(second_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        users = response.context['users']
        for user in users:
            self.assertNotIn(user, self.user.blocked_users.all())

    def test_exclude_other_users_blocking_user(self):
        second_user = User.objects.get(username='@janedoe')
        second_user.blocked_users.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        users = response.context['users']
        for user in users:
            self.assertNotIn(user, self.user.blocked_by.all())

    def test_send_friend_request(self):
        pass

    def test_card_click_redirects_to_profile(self):
        pass
