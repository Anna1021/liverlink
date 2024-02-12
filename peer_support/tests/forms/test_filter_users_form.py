"""Unit test for the FilterPeerForm"""
from django.test import TestCase
from peer_support.forms import FilterPeerForm 
from django.test import TestCase
from peer_support.models import User


class FilterPeerFormTestCase(TestCase):
    """Unit test for the FilterPeerForm"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_parent.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/other_parents.json',
    ]

    def setUp(self):
        self.users = User.objects.all()
        self.showAll = {'user_type': [],
            'gender': [],
            'language': 'any',
            'ethnicity': 'any',
            'country': 'any',
            'hospital': 'any',
            
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

    def test_hospital(self):
        form_data = self.showAll
        form_data['hospital'] = 'Airedale NHS Foundation Trust'
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
        self.assertIn(User.objects.get(username='@johndoe'), results)
        self.assertIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@janedoe'), results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), results)


    def test_patient_age_of_dio_min(self):
        min_age = 3
        form_data = self.showAll
        form_data['user_type'] = ['patient']       
        form_data['age_of_diagnosis_min'] = min_age
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertTrue(user.patient.age_of_diagnosis >= min_age)
        
    def test_patient_age_of_dio_max(self):
        max_age = 15
        form_data = self.showAll
        form_data['user_type'] = ['patient']       
        form_data['age_of_diagnosis_max'] = max_age
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertTrue(user.patient.age_of_diagnosis <= max_age)
    
    def test_patient_condition(self):
        condition = "Haemochromatosis"
        form_data = self.showAll
        form_data['user_type'] = ['patient']        
        form_data['condition'] = condition
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertEqual(user.patient.condition, condition)

    def test_parent_child_age_of_dio_min(self):
        min_age = 5
        form_data = self.showAll
        form_data['user_type'] = ['parent']        
        form_data['child_age_of_diagnosis_min'] = min_age
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertTrue(user.parent.child_age_of_diagnosis >= min_age)

    def test_parent_child_age_of_dio_max(self):
        max_age = 15
        form_data = self.showAll
        form_data['user_type'] = ['parent']
        form_data['child_age_of_diagnosis_max'] = max_age
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertTrue(user.parent.child_age_of_diagnosis <= max_age)

    def test_parent_child_condition(self):
        child_condition = "Cirrhosis"
        form_data = self.showAll
        form_data['user_type'] = ['parent']
        form_data['child_condition'] = child_condition
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertEqual(user.parent.child_condition, child_condition)
            
    def test_min_age_greater_than_max_age(self):
        form_data = self.showAll
        form_data.update({
            'min_age': 30,
            'max_age': 20,
        })
        form = FilterPeerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('min_age', form.errors)
        self.assertIn('max_age', form.errors)
        self.assertEqual(form.errors['min_age'], ['Minimum age cannot be greater than maximum age.'])
        self.assertEqual(form.errors['max_age'], ['Maximum age cannot be less than minimum age.'])

    def test_age_of_diagnosis_min_greater_than_max(self):
        form_data = self.showAll
        form_data.update({
            'age_of_diagnosis_min': 10,
            'age_of_diagnosis_max': 5, 
        })
        form = FilterPeerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('age_of_diagnosis_min', form.errors)
        self.assertIn('age_of_diagnosis_max', form.errors)
        self.assertEqual(form.errors['age_of_diagnosis_min'], ['Minimum age of diagnosis cannot be greater than maximum age of diagnosis.'])
        self.assertEqual(form.errors['age_of_diagnosis_max'], ['Maximum age of diagnosis cannot be less than minimum age of diagnosis.'])

    def test_child_age_of_diagnosis_min_greater_than_max(self):
        form_data = self.showAll
        form_data.update({
            'child_age_of_diagnosis_min': 8,
            'child_age_of_diagnosis_max': 3,
        })
        form = FilterPeerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('child_age_of_diagnosis_min', form.errors)
        self.assertIn('child_age_of_diagnosis_max', form.errors)
        self.assertEqual(form.errors['child_age_of_diagnosis_min'], ["Minimum child's age of diagnosis cannot be greater than maximum child's age of diagnosis."])
        self.assertEqual(form.errors['child_age_of_diagnosis_max'], ["Maximum child's age of diagnosis cannot be less than minimum child's age of diagnosis."])

    def test_negative_min_age(self):
        form_data = self.showAll
        form_data['min_age'] = -1
        form = FilterPeerForm(data=form_data)
        self.assertFalse(form.is_valid())
    def test_negative_max_age(self):
        form_data = self.showAll
        form_data['max_age'] = -5 
        form = FilterPeerForm(data=form_data)
        self.assertFalse(form.is_valid())
    def test_negative_age_of_diagnosis_min(self):
        form_data = self.showAll
        form_data['age_of_diagnosis_min'] = -10 
        form = FilterPeerForm(data=form_data)
        self.assertFalse(form.is_valid())
    def test_negative_age_of_diagnosis_max(self):
        form_data = self.showAll
        form_data['age_of_diagnosis_max'] = -20 
        form = FilterPeerForm(data=form_data)
        self.assertFalse(form.is_valid())
    def test_negative_child_age_of_diagnosis_min(self):
        form_data = self.showAll
        form_data['child_age_of_diagnosis_min'] = -3 
        form = FilterPeerForm(data=form_data)
        self.assertFalse(form.is_valid())
    def test_negative_child_age_of_diagnosis_max(self):
        form_data = self.showAll
        form_data['child_age_of_diagnosis_max'] = -7 
        form = FilterPeerForm(data=form_data)
        self.assertFalse(form.is_valid())