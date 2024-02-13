"""Tests of the deactivate user view."""
import datetime
from django.db import IntegrityError
from django.test import TestCase
from django.contrib import messages
from django.urls import reverse
from peer_support.models import User, Patient, Parent

class DeactivateUserViewTestCase(TestCase):
    """Tests of the deactivate user view."""

    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/default_patient.json',
                'peer_support/tests/fixtures/default_parent.json']

    def setUp(self):
        self.url = reverse('deactivate_user')
        self.user = User.objects.get(username='@johndoe')
        self.patient = Patient.objects.get(username='@johndoe')
        self.parent = Parent.objects.get(username='@johndoe')

    def test_deactivate_user_url(self):
        self.assertEqual(self.url,'/deactivate_user/')

    def test_get_deactivate_user_unsuccessful(self):
        """Ensure only post requests can be made to 'deactivate_user' - url can only be accessed through redirect."""
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_successful_user_deactivation(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self.user.is_active)
        response = self.client.post(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_patient_deactivation_deactivates_user_and_patient_objects(self):
        patient_user = Patient.objects.get(id=self.patient.id)
        self.client.login(username=self.patient.username, password='Password123')
        self.assertTrue(patient_user.is_active)
        self.assertTrue(self.patient.is_active)
        response = self.client.post(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        patient_user.refresh_from_db()
        self.patient.refresh_from_db()
        self.assertFalse(patient_user.is_active)
        self.assertFalse(self.patient.is_active)

    def test_parent_deactivation_deactivates_user_and_parent_objects(self):
        parent_user = Parent.objects.get(id=self.parent.id)
        self.client.login(username=self.parent.username, password='Password123')
        self.assertTrue(parent_user.is_active)
        self.assertTrue(self.parent.is_active)
        response = self.client.post(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        parent_user.refresh_from_db()
        self.parent.refresh_from_db()
        self.assertFalse(parent_user.is_active)
        self.assertFalse(self.parent.is_active)

    def test_user_still_exists_after_deactivation(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self.user.is_active)
        self.client.post(self.url, follow=True)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertTrue(User.objects.all().contains(self.user))
    
    def test_new_user_cannot_have_same_unique_fields_as_deactivated_user(self):
        self.client.login(username=self.user.username, password='Password123')
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
                                    age_of_diagnosis=20)

    def test_user_cannot_log_in_after_deactivation(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self.user.is_active)
        self.client.post(self.url, follow=True)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        login = self.client.login(username=self.user.username, password='Password123')
        self.assertFalse(login)
