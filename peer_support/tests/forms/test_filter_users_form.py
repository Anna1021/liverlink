from django.test import TestCase
from peer_support.forms import FilterPeerForm 
from django.test import TestCase
from peer_support.models import User


class FilterPeerFormTestCase(TestCase):
    """Test for the FilterPeerForm"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_parent.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
    ]

    def setUp(self):
        self.users = User.objects.all()
        self.showAll = {'user_type': [],
            'gender': [],
            'language': 'any',
            'ethnicity': 'any',
            'country': 'any',
        }

    def test_form_initialization(self):
        form = FilterPeerForm()
        self.assertTrue(form.is_bound is False)
        self.assertIn('user_type', form.fields)
        self.assertIn('min_age', form.fields)
        self.assertIn('max_age', form.fields)
        self.assertIn('language', form.fields)
        self.assertIn('ethnicity', form.fields)
        self.assertIn('gender', form.fields)
        self.assertIn('country', form.fields)
    
    def test_filter_by_user_type_patient(self):
        form_data = self.showAll
        form_data['user_type'] = ['patient']
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(all(user.patient for user in results))
        for user in results:
            try:
                parent_exists = user.parent
                self.fail("Found a user marked as a parent in patient-only filter.") 
            except user._meta.model.parent.RelatedObjectDoesNotExist:
                pass 
    
    def test_filter_by_user_type_parent(self):
        form_data = self.showAll
        form_data['user_type'] = ['parent']
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(all(user.parent for user in results))
        for user in results:
            try:
                patient_exists = user.patient
                self.fail("Found a user marked as a patient in patient-only filter.") 
            except user._meta.model.patient.RelatedObjectDoesNotExist:
                pass 

    def test_min_age(self):
        form_data = self.showAll
        form_data['min_age'] = 25
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
        self.assertIn(User.objects.get(username='@johndoe'), results)
        self.assertIn(User.objects.get(username='@peterpickles'), results)
        self.assertNotIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@janedoe'), results)

    def test_max_age(self):
        form_data = self.showAll
        form_data['max_age'] = 25
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
        self.assertIn(User.objects.get(username='@janedoe'), results)
        self.assertIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), results)
        self.assertNotIn(User.objects.get(username='@johndoe'), results)

    def test_language(self):
        form_data = self.showAll
        form_data['language'] = 'en'
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
        self.assertIn(User.objects.get(username='@johndoe'), results)
        self.assertNotIn(User.objects.get(username='@janedoe'), results)
        self.assertNotIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), results)
        
    def test_ethnicity(self):
        form_data = self.showAll
        form_data['ethnicity'] = 'BR'
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
        self.assertIn(User.objects.get(username='@johndoe'), results)
        self.assertNotIn(User.objects.get(username='@janedoe'), results)
        self.assertNotIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), results)

    def test_gender(self):
        form_data = self.showAll
        form_data['gender'] = ['M']
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
        self.assertIn(User.objects.get(username='@johndoe'), results)
        self.assertNotIn(User.objects.get(username='@janedoe'), results)
        self.assertNotIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), results)

    def test_country(self):
        form_data = self.showAll
        form_data['country'] = 'GB'
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
        self.assertIn(User.objects.get(username='@johndoe'), results)
        self.assertIn(User.objects.get(username='@janedoe'), results)
        self.assertNotIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), results)