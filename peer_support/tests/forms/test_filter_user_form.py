"""Unit test of the filter peer form"""
from django.test import TestCase
from peer_support.forms import FilterUserForm 
from peer_support.models import User

class FilterUserFormTestCase(TestCase):
    """Unit test of the filter peer form"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_mentor.json',
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
        form = FilterUserForm()
        self.assertTrue(form.is_bound is False)
        self.assertIn('user_type', form.fields)
        self.assertIn('min_age', form.fields)
        self.assertIn('max_age', form.fields)
        self.assertIn('language', form.fields)
        self.assertIn('ethnicity', form.fields)
        self.assertIn('gender', form.fields)
        self.assertIn('country', form.fields)
    
    def test_form_validity(self):
        form_data = {
            'user_type': ['PT', 'PR'],
            'gender': ['M', 'F'],
            'language': 'fr',
            'ethnicity': 'BD',
            'location': 'BD',
            'hospital': 'Guy’s and St Thomas’ NHS Foundation Trust',
            'min_age': 18,
            'max_age': 65
        }
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_show_all(self):
        form = FilterUserForm(data=self.showAll)
        self.assertTrue(form.is_valid(), "Form should be valid with 'show all' settings")
        results = form.filter_users(self.users)
        expected_user_count = self.users.count()
        self.assertEqual(results.count(), expected_user_count, f"Expected {expected_user_count} users, but got {results.count()}")

    def test_filter_by_user_type_patient(self):
        form_data = self.showAll
        form_data['user_type'] = ['PT']
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(all(user.patient for user in results))
    
    def test_filter_by_user_type_parent(self):
        form_data = self.showAll
        form_data['user_type'] = ['PR']
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(all(user.parent for user in results))

    def test_min_age(self):
        form_data = self.showAll
        form_data['min_age'] = 25
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
        self.assertIn(User.objects.get(username='@peterpickles'), results)
        self.assertNotIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@janedoe'), results)

    def test_max_age(self):
        form_data = self.showAll
        form_data['max_age'] = 25
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
        self.assertIn(User.objects.get(username='@janedoe'), results)
        self.assertIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), results)

    def test_language(self):
        form_data = self.showAll
        form_data['language'] = 'en'
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
        self.assertIn(User.objects.get(username='@janedoe'), results)
        self.assertNotIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), results)
        
    def test_ethnicity(self):
        form_data = self.showAll
        form_data['ethnicity'] = 'BR'
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
        self.assertIn(User.objects.get(username='@janedoe'), results)
        self.assertNotIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), results)

    def test_gender(self):
        form_data = self.showAll
        form_data['gender'] = ['M']
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
        self.assertNotIn(User.objects.get(username='@janedoe'), results)
        self.assertNotIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), results)

    def test_country(self):
        form_data = self.showAll
        form_data['country'] = 'GB'
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
        self.assertIn(User.objects.get(username='@janedoe'), results)
        self.assertNotIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), results)

    def test_hospital(self):
        form_data = self.showAll
        form_data['hospital'] = 'Airedale NHS Foundation Trust'
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
        self.assertIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@janedoe'), results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), results)

    def test_patient_age_of_dio_min(self):
        min_age = 3
        form_data = self.showAll
        form_data['user_type'] = ['PT']       
        form_data['age_of_diagnosis_min'] = min_age
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertTrue(user.patient.age_of_diagnosis >= min_age)
        
    def test_patient_age_of_dio_max(self):
        max_age = 15
        form_data = self.showAll
        form_data['user_type'] = ['PT']       
        form_data['age_of_diagnosis_max'] = max_age
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertTrue(user.patient.age_of_diagnosis <= max_age)
    
    def test_patient_condition(self):
        condition = "Haemochromatosis"
        form_data = self.showAll
        form_data['user_type'] = ['PT']        
        form_data['condition'] = condition
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertEqual(user.patient.condition, condition)

    def test_patient_transplant_status(self):
        transplant = "Y"
        form_data = self.showAll
        form_data['user_type'] = ['PT']        
        form_data['transplant'] = transplant
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertEqual(user.patient.transplant, transplant)

    def test_parent_child_age_of_dio_min(self):
        min_age = 5
        form_data = self.showAll
        form_data['user_type'] = ['PR']        
        form_data['child_age_of_diagnosis_min'] = min_age
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertTrue(user.parent.child_age_of_diagnosis >= min_age)

    def test_parent_child_age_of_dio_max(self):
        max_age = 15
        form_data = self.showAll
        form_data['user_type'] = ['PR']
        form_data['child_age_of_diagnosis_max'] = max_age
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertTrue(user.parent.child_age_of_diagnosis <= max_age)

    def test_parent_child_condition(self):
        child_condition = "Cirrhosis"
        form_data = self.showAll
        form_data['user_type'] = ['PR']
        form_data['child_condition'] = child_condition
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertEqual(user.parent.child_condition, child_condition)

    def test_child_transplant_status(self):
        child_transplant = "Y"
        form_data = self.showAll
        form_data['user_type'] = ['PR']        
        form_data['child_transplant'] = child_transplant
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertEqual(user.parent.child_transplant, child_transplant)
    
    def test_mentor_age_of_dio_min(self):
        min_age = 5
        form_data = self.showAll
        form_data['user_type'] = ['MT']        
        form_data['mentor_age_of_diagnosis_min'] = min_age
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertTrue(user.mentor.age_of_diagnosis >= min_age)

    def test_mentor_age_of_dio_max(self):
        max_age = 50
        form_data = self.showAll
        form_data['user_type'] = ['MT']
        form_data['mentor_age_of_diagnosis_max'] = max_age
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertTrue(user.mentor.age_of_diagnosis <= max_age)

    def test_mentor_condition(self):
        mentor_condition = "Hepatitis A"
        form_data = self.showAll
        form_data['user_type'] = ['MT']
        form_data['mentor_condition'] = mentor_condition
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertEqual(user.mentor.condition, mentor_condition)

    def test_mentor_transplant_status(self):
        transplant = "Y"
        form_data = self.showAll
        form_data['user_type'] = ['MT']        
        form_data['transplant'] = transplant
        form = FilterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertEqual(user.mentor.transplant, transplant)
 
    def test_min_age_greater_than_max_age(self):
        form_data = self.showAll
        form_data.update({
            'min_age': 30,
            'max_age': 20,
        })
        form = FilterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('min_age' in form.errors)
        self.assertTrue('max_age' in form.errors)

    def test_age_of_diagnosis_min_greater_than_max(self):
        form_data = self.showAll
        form_data.update({
            'age_of_diagnosis_min': 10,
            'age_of_diagnosis_max': 5,
        })
        form = FilterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('age_of_diagnosis_min' in form.errors)
        self.assertTrue('age_of_diagnosis_max' in form.errors)

    def test_child_age_of_diagnosis_min_greater_than_max(self):
        form_data = self.showAll
        form_data.update({
            'child_age_of_diagnosis_min': 8,
            'child_age_of_diagnosis_max': 3,
        })
        form = FilterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('child_age_of_diagnosis_min' in form.errors)
        self.assertTrue('child_age_of_diagnosis_max' in form.errors)

    def test_mentor_age_of_diagnosis_min_greater_than_max(self):
        form_data = self.showAll
        form_data.update({
            'mentor_age_of_diagnosis_min': 10,
            'mentor_age_of_diagnosis_max': 5,
        })
        form = FilterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('mentor_age_of_diagnosis_min' in form.errors)
        self.assertTrue('mentor_age_of_diagnosis_max' in form.errors)


    def test_negative_min_age(self):
        form_data = self.showAll
        form_data['min_age'] = -1
        form = FilterUserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_negative_max_age(self):
        form_data = self.showAll
        form_data['max_age'] = -5 
        form = FilterUserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_negative_age_of_diagnosis_min(self):
        form_data = self.showAll
        form_data['age_of_diagnosis_min'] = -10 
        form = FilterUserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_negative_age_of_diagnosis_max(self):
        form_data = self.showAll
        form_data['age_of_diagnosis_max'] = -20 
        form = FilterUserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_negative_child_age_of_diagnosis_min(self):
        form_data = self.showAll
        form_data['child_age_of_diagnosis_min'] = -3 
        form = FilterUserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_negative_child_age_of_diagnosis_max(self):
        form_data = self.showAll
        form_data['child_age_of_diagnosis_max'] = -7 
        form = FilterUserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_mentor_age_of_diagnosis_min(self):
        form_data = self.showAll
        form_data['mentor_age_of_diagnosis_min'] = -3 
        form = FilterUserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_negative_mentor_of_diagnosis_max(self):
        form_data = self.showAll
        form_data['mentor_age_of_diagnosis_max'] = -7 
        form = FilterUserForm(data=form_data)
        self.assertFalse(form.is_valid())