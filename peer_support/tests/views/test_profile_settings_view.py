"""Tests for the profile view."""
import datetime
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from peer_support.forms import PatientForm, ParentForm
from peer_support.models import Patient, Parent
from peer_support.tests.helpers import reverse_with_next

class ProfileViewTest(TestCase):
    """Test suite for the profile view."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_patient.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_parents.json',
    ]

    def setUp(self):
        self.patient = Patient.objects.get(username='@johndoe')
        self.parent = Parent.objects.get(username='@janedoe')
        self.url = reverse('profile')
        self.patient_form_input = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': '@johndoe',
            'email': 'johndoe@example.org',
            'date_of_birth': '1990-01-01',
            'gender': 'M',
            'location': 'US',
            'ethnicity': 'RO',
            'language': 'en',
            'bio': 'I am a test patient.',
            'condition': 'Haemochromatosis',
            'age_of_diagnosis': 21,
        }
        self.parent_form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': '@janedoe',
            'email': 'janedoe@example.org',
            'date_of_birth': '1991-01-01',
            'gender': 'F',
            'location': 'US',
            'ethnicity': 'RO',
            'language': 'en',
            'bio': 'I am a test patient.',
            'child_condition': 'Haemochromatosis',
            'child_age_of_diagnosis': 21,
        }

    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/')

    def test_get_patient_form_when_current_user_is_patient(self):
        self.client.login(username=self.patient.username, password='Password123')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PatientForm))

    def test_get_parent_form_when_current_user_is_parent(self):
        self.client.login(username=self.parent.username, password='Password123')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ParentForm))   

    def test_get_profile(self):
        self.client.login(username=self.patient.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PatientForm))
        self.assertEqual(form.instance, self.patient) #AssertionError: <SimpleLazyObject: <User: @johndoe>> != <Patient: @johndoe>

    def test_get_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_unsuccesful_profile_update_for_patient(self):
        self.client.login(username=self.patient.username, password='Password123')
        self.patient_form_input['username'] = 'BAD_USERNAME'
        before_count = Patient.objects.count()
        response = self.client.post(self.url, self.patient_form_input)
        after_count = Patient.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PatientForm))
        self.assertTrue(form.is_bound)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.username, '@johndoe')
        self.assertEqual(self.patient.first_name, 'John')
        self.assertEqual(self.patient.last_name, 'Doe')
        self.assertEqual(self.patient.email, 'johndoe@example.org')
        self.assertEqual(self.patient.date_of_birth, datetime.date(1990, 1, 1)),
        self.assertEqual(self.patient.gender, 'M'),
        self.assertEqual(self.patient.location, 'GB'),
        self.assertEqual(self.patient.ethnicity, 'BR'),
        self.assertEqual(self.patient.language, 'en'),
        self.assertEqual(self.patient.bio, "I'm a test user"),
        self.assertEqual(self.patient.condition, "Hepatitis"),
        self.assertEqual(self.patient.age_of_diagnosis, 20)

    def test_unsuccesful_profile_update_for_parent(self):
        self.client.login(username=self.parent.username, password='Password123')
        self.parent_form_input['username'] = 'BAD_USERNAME'
        before_count = Parent.objects.count()
        response = self.client.post(self.url, self.parent_form_input)
        after_count = Parent.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ParentForm))
        self.assertTrue(form.is_bound)
        self.parent.refresh_from_db()
        self.assertEqual(self.parent.username, '@janedoe')
        self.assertEqual(self.parent.first_name, 'Jane')
        self.assertEqual(self.parent.last_name, 'Doe')
        self.assertEqual(self.parent.email, 'janedoe@example.org')
        self.assertEqual(self.parent.date_of_birth, datetime.date(2004, 3, 2)),
        self.assertEqual(self.parent.gender, 'F'),
        self.assertEqual(self.parent.location, 'GB'),
        self.assertEqual(self.parent.ethnicity, 'OM'),
        self.assertEqual(self.parent.language, 'en'),
        self.assertEqual(self.parent.bio, "Hi, I'm Jane Doe"),
        self.assertEqual(self.parent.child_condition, "Biliary atresia"),
        self.assertEqual(self.parent.child_age_of_diagnosis, 2)

    def test_unsuccessful_profile_update_due_to_duplicate_username(self):
        self.client.login(username=self.patient.username, password='Password123')
        self.patient_form_input['username'] = '@janedoe'
        before_count = Patient.objects.count()
        response = self.client.post(self.url, self.patient_form_input)
        after_count = Patient.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PatientForm))
        self.assertTrue(form.is_bound)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.username, '@johndoe')
        self.assertEqual(self.patient.first_name, 'John')
        self.assertEqual(self.patient.last_name, 'Doe')
        self.assertEqual(self.patient.email, 'johndoe@example.org')
        self.assertEqual(self.patient.date_of_birth, datetime.date(1990, 1, 1)),
        self.assertEqual(self.patient.gender, 'M'),
        self.assertEqual(self.patient.location, 'GB'),
        self.assertEqual(self.patient.ethnicity, 'BR'),
        self.assertEqual(self.patient.language, 'en'),
        self.assertEqual(self.patient.bio, "I'm a test user"),
        self.assertEqual(self.patient.condition, "Hepatitis"),
        self.assertEqual(self.patient.age_of_diagnosis, 20)

    def test_succesful_profile_update_for_patient(self):
        self.client.login(username=self.patient.username, password='Password123')
        before_count = Patient.objects.count()
        response = self.client.post(self.url, self.patient_form_input, follow=True)
        after_count = Patient.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.username, '@johndoe')
        self.assertEqual(self.patient.first_name, 'John')
        self.assertEqual(self.patient.last_name, 'Doe')
        self.assertEqual(self.patient.email, 'johndoe@example.org')
        self.assertEqual(self.patient.date_of_birth, datetime.date(1990, 1, 1)),
        self.assertEqual(self.patient.gender, 'M'),
        self.assertEqual(self.patient.location, 'US'),
        self.assertEqual(self.patient.ethnicity, 'RO'),
        self.assertEqual(self.patient.language, 'en'),
        self.assertEqual(self.patient.bio, "I am a test patient."),
        self.assertEqual(self.patient.condition, "Haemochromatosis"),
        self.assertEqual(self.patient.age_of_diagnosis, 21)

    def test_succesful_profile_update_for_parent(self):
        self.client.login(username=self.parent.username, password='Password123')
        before_count = Parent.objects.count()
        response = self.client.post(self.url, self.parent_form_input, follow=True)
        after_count = Parent.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.parent.refresh_from_db()
        self.assertEqual(self.parent.username, '@janedoe')
        self.assertEqual(self.parent.first_name, 'Jane')
        self.assertEqual(self.parent.last_name, 'Doe')
        self.assertEqual(self.parent.email, 'janedoe@example.org')
        self.assertEqual(self.parent.date_of_birth, datetime.date(1991, 1, 1)),
        self.assertEqual(self.parent.gender, 'F'),
        self.assertEqual(self.parent.location, 'US'),
        self.assertEqual(self.parent.ethnicity, 'RO'),
        self.assertEqual(self.parent.language, 'en'),
        self.assertEqual(self.parent.bio, "I am a test patient."),
        self.assertEqual(self.parent.condition, "Haemochromatosis"),
        self.assertEqual(self.parent.age_of_diagnosis, 21)

    def test_post_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.patient_form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
