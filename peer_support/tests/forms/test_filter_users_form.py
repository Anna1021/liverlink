"""Unit test for the FilterPeerForm"""
from django.test import TestCase
from peer_support.forms import FilterPeerForm 
from django.test import TestCase
from peer_support.models import User


class FilterPeerFormTestCase(TestCase):
    """Unit test for the FilterPeerForm"""

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
        form = FilterPeerForm()
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
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_show_all(self):
        form = FilterPeerForm(data=self.showAll)
        self.assertTrue(form.is_valid(), "Form should be valid with 'show all' settings")

        results = form.filter_users(self.users)
        expected_user_count = self.users.count()
        self.assertEqual(results.count(), expected_user_count, f"Expected {expected_user_count} users, but got {results.count()}")


    def test_filter_by_user_type_patient(self):
        form_data = self.showAll
        form_data['user_type'] = ['PT']
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
        form_data['user_type'] = ['PR']
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(all(user.parent for user in results))
        for user in results:
            try:
                patient_exists = user.patient
                self.fail("Found a user marked as a patient in parent-only filter.") 
            except user._meta.model.patient.RelatedObjectDoesNotExist:
                pass 

    def test_filter_by_user_type_professional(self):
        form_data = self.showAll
        form_data['user_type'] = ['PF']
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(all(user.professional for user in results))
        for user in results:
            try:
                patient_exists = user.patient
                self.fail("Found a user marked as a patient in professional-only filter.") 
            except user._meta.model.patient.RelatedObjectDoesNotExist:
                pass 

    def test_min_age(self):
        form_data = self.showAll
        form_data['min_age'] = 25
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
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

    def test_language(self):
        form_data = self.showAll
        form_data['language'] = 'en'
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
        self.assertIn(User.objects.get(username='@janedoe'), results)
        self.assertNotIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), results)
        
    def test_ethnicity(self):
        form_data = self.showAll
        form_data['ethnicity'] = 'BR'
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
        self.assertIn(User.objects.get(username='@janedoe'), results)
        self.assertNotIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), results)

    def test_gender(self):
        form_data = self.showAll
        form_data['gender'] = ['M']
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        self.assertTrue(results.exists())
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
        self.assertIn(User.objects.get(username='@petrapickles'), results)
        self.assertNotIn(User.objects.get(username='@janedoe'), results)
        self.assertNotIn(User.objects.get(username='@peterpickles'), results)

    def test_patient_age_of_dio_min(self):
        min_age = 3
        form_data = self.showAll
        form_data['user_type'] = ['PT']       
        form_data['age_of_diagnosis_min'] = min_age
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertTrue(user.patient.age_of_diagnosis >= min_age)
        
    def test_patient_age_of_dio_max(self):
        max_age = 15
        form_data = self.showAll
        form_data['user_type'] = ['PT']       
        form_data['age_of_diagnosis_max'] = max_age
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertTrue(user.patient.age_of_diagnosis <= max_age)
    
    def test_patient_condition(self):
        condition = "Haemochromatosis"
        form_data = self.showAll
        form_data['user_type'] = ['PT']        
        form_data['condition'] = condition
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertEqual(user.patient.condition, condition)

    def test_patient_transplant_status(self):
        transplant = "Y"
        form_data = self.showAll
        form_data['user_type'] = ['PT']        
        form_data['transplant'] = transplant
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertEqual(user.patient.transplant, transplant)

    def test_parent_child_age_of_dio_min(self):
        min_age = 5
        form_data = self.showAll
        form_data['user_type'] = ['PR']        
        form_data['child_age_of_diagnosis_min'] = min_age
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertTrue(user.parent.child_age_of_diagnosis >= min_age)

    def test_parent_child_age_of_dio_max(self):
        max_age = 15
        form_data = self.showAll
        form_data['user_type'] = ['PR']
        form_data['child_age_of_diagnosis_max'] = max_age
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertTrue(user.parent.child_age_of_diagnosis <= max_age)

    def test_parent_child_condition(self):
        child_condition = "Cirrhosis"
        form_data = self.showAll
        form_data['user_type'] = ['PR']
        form_data['child_condition'] = child_condition
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertEqual(user.parent.child_condition, child_condition)

    def test_professional_expertise(self):
        expertise = "Cirrhosis"
        form_data = self.showAll
        form_data['user_type'] = ['PF']
        form_data['expertise'] = expertise
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertEqual(user.professional.expertise, expertise)

    def test_child_transplant_status(self):
        child_transplant = "Y"
        form_data = self.showAll
        form_data['user_type'] = ['PR']        
        form_data['child_transplant'] = child_transplant
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertEqual(user.parent.child_transplant, child_transplant)
    
    def test_mentor_age_of_dio_min(self):
        min_age = 5
        form_data = self.showAll
        form_data['user_type'] = ['MT']        
        form_data['mentor_age_of_diagnosis_min'] = min_age
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertTrue(user.mentor.age_of_diagnosis >= min_age)

    def test_mentor_age_of_dio_max(self):
        max_age = 50
        form_data = self.showAll
        form_data['user_type'] = ['MT']
        form_data['mentor_age_of_diagnosis_max'] = max_age
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertTrue(user.mentor.age_of_diagnosis <= max_age)

    def test_mentor_condition(self):
        mentor_condition = "Hepatitis A"
        form_data = self.showAll
        form_data['user_type'] = ['MT']
        form_data['mentor_condition'] = mentor_condition
        form = FilterPeerForm(data=form_data)
        self.assertTrue(form.is_valid())
        results = form.filter_users(self.users)
        for user in results:
            self.assertEqual(user.mentor.condition, mentor_condition)

    def test_mentor_transplant_status(self):
        transplant = "Y"
        form_data = self.showAll
        form_data['user_type'] = ['MT']        
        form_data['transplant'] = transplant
        form = FilterPeerForm(data=form_data)
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

    def test_mentor_age_of_diagnosis_min_greater_than_max(self):
        form_data = self.showAll
        form_data.update({
            'mentor_age_of_diagnosis_min': 10,
            'mentor_age_of_diagnosis_max': 5, 
        })
        form = FilterPeerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('mentor_age_of_diagnosis_min', form.errors)
        self.assertIn('mentor_age_of_diagnosis_max', form.errors)
        self.assertEqual(form.errors['mentor_age_of_diagnosis_min'], ["Minimum mentor's age of diagnosis cannot be greater than maximum mentor's age of diagnosis."])
        self.assertEqual(form.errors['mentor_age_of_diagnosis_max'], ["Maximum mentor's age of diagnosis cannot be less than minimum mentor's age of diagnosis."])

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

    def test_mentor_age_of_diagnosis_min(self):
        form_data = self.showAll
        form_data['mentor_age_of_diagnosis_min'] = -3 
        form = FilterPeerForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_negative_mentor_of_diagnosis_max(self):
        form_data = self.showAll
        form_data['mentor_age_of_diagnosis_max'] = -7 
        form = FilterPeerForm(data=form_data)
        self.assertFalse(form.is_valid())

    

    