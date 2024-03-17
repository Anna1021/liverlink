"""Tests of the deactivate user view."""
import datetime
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from peer_support.models import User, Patient, Parent, Mentor

class DeactivateUserViewTestCase(TestCase):
    """Tests of the deactivate user view."""

    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/other_patients.json',
                'peer_support/tests/fixtures/other_parents.json',
                'peer_support/tests/fixtures/other_mentors.json']

    def setUp(self):
        self.url = reverse('deactivate_user')
        self.user = User.objects.get(username='@johndoe')
        self.patient = Patient.objects.get(username='@janedoe')
        self.parent = Parent.objects.get(username='@alexsmith')
        self.mentor = Mentor.objects.get(username='@lindajohnson')
        self.client.force_login(self.user)

    def test_deactivate_user_url(self):
        self.assertEqual(self.url,'/deactivate_user/')

    def test_get_deactivate_user_unsuccessful(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_successful_user_deactivation(self):
        self.assertTrue(self.user.is_active)
        response = self.client.post(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_patient_deactivation_deactivates_user_and_patient_objects(self):
        self.client.logout()
        patient_user = User.objects.get(id=self.patient.id)
        self.client.force_login(self.patient)
        self.assertTrue(patient_user.is_active)
        self.assertTrue(self.patient.is_active)
        response = self.client.post(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        patient_user.refresh_from_db()
        self.patient.refresh_from_db()
        self.assertFalse(patient_user.is_active)
        self.assertFalse(self.patient.is_active)

    def test_parent_deactivation_deactivates_user_and_parent_objects(self):
        self.client.logout()
        parent_user = User.objects.get(id=self.parent.id)
        self.client.force_login(self.parent)
        self.assertTrue(parent_user.is_active)
        self.assertTrue(self.parent.is_active)
        response = self.client.post(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        parent_user.refresh_from_db()
        self.parent.refresh_from_db()
        self.assertFalse(parent_user.is_active)
        self.assertFalse(self.parent.is_active)

    def test_mentor_deactivation_deactivates_user_and_mentor_objects(self):
        self.client.logout()
        mentor_user = User.objects.get(id=self.mentor.id)
        self.client.force_login(mentor_user)
        self.assertTrue(mentor_user.is_active)
        self.assertTrue(self.mentor.is_active)
        response = self.client.post(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        mentor_user.refresh_from_db()
        self.mentor.refresh_from_db()
        self.assertFalse(mentor_user.is_active)
        self.assertFalse(self.mentor.is_active)

    def test_user_still_exists_after_deactivation(self):
        self.assertTrue(self.user.is_active)
        self.client.post(self.url, follow=True)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertTrue(User.objects.all().contains(self.user))
    
    def test_new_user_cannot_have_same_unique_fields_as_deactivated_user(self):
        self.assertTrue(self.user.is_active)
        self.client.post(self.url, follow=True)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        with self.assertRaises(IntegrityError):
            Patient.objects.create(username=self.user.username, 
                                    first_name="test", 
                                    last_name="test", 
                                    email=self.user.email,
                                    password="Password123",
                                    date_of_birth=datetime.date(1990,1,1),
                                    gender="M",
                                    location="GB",
                                    ethnicity="BR",
                                    language="en",
                                    bio="abc",
                                    condition="Hepatitis",
                                    transplant="N",
                                    age_of_diagnosis=20)

    def test_user_cannot_log_in_after_deactivation(self):
        self.assertTrue(self.user.is_active)
        self.client.post(self.url, follow=True)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        login = self.client.force_login(self.user)
        self.assertFalse(login)
