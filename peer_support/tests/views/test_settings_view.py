"""Tests for the profile settings view."""
import datetime
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from peer_support.forms import PatientForm, ParentForm, MentorForm
from peer_support.models import Patient, Parent, Mentor
from peer_support.tests.helpers import reverse_with_next

class SettingsViewTest(TestCase):
    """Test suite for the profile settings view."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_parent.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/default_user_profile.json',
        'peer_support/tests/fixtures/other_user_profiles.json',
    ]

    def setUp(self):
        self.parent = Parent.objects.get(username='@johndoe')
        self.patient = Patient.objects.get(username='@janedoe')
        Mentor.objects.create_user(first_name='Test',
                                   last_name='Mentor',
                                   username='@testmentor',
                                   email='testmentor@example.org',
                                   password='Password123',
                                   date_of_birth='1980-01-01',
                                   gender='F',
                                   location='FR',
                                   ethnicity='RO',
                                   language='en',
                                   bio='I am a test mentor.',
                                   condition='Cirrhosis',
                                   age_of_diagnosis=15,
                                   transplant='N',
                                   referral_code='TEST123')
        self.mentor = Mentor.objects.get(username='@testmentor')
        self.url = reverse('settings')
        self.parent_form_input = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': '@johndoe',
            'email': 'johndoe@example.org',
            'date_of_birth': '1990-01-01',
            'gender': 'M',
            'location': 'US',
            'ethnicity': 'RO',
            'language': 'en',
            'bio': 'I am a test parent.',
            'child_condition': 'Haemochromatosis',
            'child_transplant': 'N',
            'child_age_of_diagnosis': 21,
        }
        self.patient_form_input = {
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
            'condition': 'Haemochromatosis',
            'transplant': 'N',
            'age_of_diagnosis': 21,
        }
        self.mentor_form_input = {
            'first_name': 'Test',
            'last_name': 'Mentor',
            'username': '@testmentor1',
            'email': 'testmentor@example.org',
            'date_of_birth': '1991-01-01',
            'gender': 'M',
            'location': 'US',
            'ethnicity': 'RO',
            'language': 'en',
            'bio': 'I am a test mentor.',
            'condition': 'Haemochromatosis',
            'age_of_diagnosis': 21,
            'transplant': 'N',
            'referral_code': 'TEST123'
        }

    def test_profile_url(self):
        self.assertEqual(self.url, '/settings/')

    def test_get_patient_form_when_current_user_is_patient(self):
        self.client.login(username=self.patient.username, password='Password123')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'settings.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PatientForm))

    def test_get_parent_form_when_current_user_is_parent(self):
        self.client.login(username=self.parent.username, password='Password123')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'settings.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ParentForm))  

    def test_get_mentor_form_when_current_user_is_mentor(self):
        self.client.login(username=self.mentor.username, password='Password123')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'settings.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, MentorForm))    

    def test_get_profile(self):
        self.client.login(username=self.patient.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PatientForm))
        self.assertEqual(form.instance, self.patient)

    def test_get_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_unsuccessful_profile_update_for_patient(self):
        self.client.login(username=self.patient.username, password='Password123')
        self.patient_form_input['username'] = 'BAD_USERNAME'
        before_count = Patient.objects.count()
        response = self.client.post(self.url, self.patient_form_input)
        after_count = Patient.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PatientForm))
        self.assertTrue(form.is_bound)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.username, '@janedoe')
        self.assertEqual(self.patient.first_name, 'Jane')
        self.assertEqual(self.patient.last_name, 'Doe')
        self.assertEqual(self.patient.email, 'janedoe@example.org')
        self.assertEqual(self.patient.date_of_birth, datetime.date(2004, 3, 2)),
        self.assertEqual(self.patient.gender, 'F'),
        self.assertEqual(self.patient.location, 'GB'),
        self.assertEqual(self.patient.ethnicity, 'BR'),
        self.assertEqual(self.patient.language, 'en'),
        self.assertEqual(self.patient.bio, "Hi, I'm Jane Doe"),
        self.assertEqual(self.patient.condition, "Biliary atresia"),
        self.assertEqual(self.patient.age_of_diagnosis, 2),

    def test_unsuccessful_profile_update_for_parent(self):
        self.client.login(username=self.parent.username, password='Password123')
        self.parent_form_input['username'] = 'BAD_USERNAME'
        before_count = Parent.objects.count()
        response = self.client.post(self.url, self.parent_form_input)
        after_count = Parent.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ParentForm))
        self.assertTrue(form.is_bound)
        self.parent.refresh_from_db()
        self.assertEqual(self.parent.username, '@johndoe')
        self.assertEqual(self.parent.first_name, 'John')
        self.assertEqual(self.parent.last_name, 'Doe')
        self.assertEqual(self.parent.email, 'johndoe@example.org')
        self.assertEqual(self.parent.date_of_birth, datetime.date(1990, 1, 1)),
        self.assertEqual(self.parent.gender, 'M'),
        self.assertEqual(self.parent.location, 'GB'),
        self.assertEqual(self.parent.ethnicity, 'BR'),
        self.assertEqual(self.parent.language, 'en'),
        self.assertEqual(self.parent.bio, "I'm a test user"),
        self.assertEqual(self.parent.child_condition, "Hepatitis"),
        self.assertEqual(self.parent.child_age_of_diagnosis, 20),
        self.assertEqual(self.parent.child_transplant, 'N')

    def test_unsuccessful_profile_update_for_mentor(self):
        self.client.login(username=self.mentor.username, password='Password123')
        self.mentor_form_input['username'] = 'BAD_USERNAME'
        before_count = Mentor.objects.count()
        response = self.client.post(self.url, self.mentor_form_input)
        after_count = Mentor.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, MentorForm))
        self.assertTrue(form.is_bound)
        self.mentor.refresh_from_db()
        self.assertEqual(self.mentor.username, '@testmentor')
        self.assertEqual(self.mentor.first_name, 'Test')
        self.assertEqual(self.mentor.last_name, 'Mentor')
        self.assertEqual(self.mentor.email, 'testmentor@example.org')
        self.assertEqual(self.mentor.date_of_birth, datetime.date(1980, 1, 1)),
        self.assertEqual(self.mentor.gender, 'F'),
        self.assertEqual(self.mentor.location, 'FR')
        self.assertEqual(self.mentor.ethnicity, 'RO'),
        self.assertEqual(self.mentor.language, 'en'),
        self.assertEqual(self.mentor.bio, "I am a test mentor."),
        self.assertEqual(self.mentor.condition, 'Cirrhosis'),
        self.assertEqual(self.mentor.age_of_diagnosis, 15),
        self.assertEqual(self.mentor.transplant, 'N'),
        self.assertEqual(self.mentor.referral_code, 'TEST123')

    def test_unsuccessful_profile_update_due_to_duplicate_username(self):
        self.client.login(username=self.patient.username, password='Password123')
        self.patient_form_input['username'] = '@johndoe'
        before_count = Patient.objects.count()
        response = self.client.post(self.url, self.patient_form_input)
        after_count = Patient.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PatientForm))
        self.assertTrue(form.is_bound)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.username, '@janedoe')
        self.assertEqual(self.patient.first_name, 'Jane')
        self.assertEqual(self.patient.last_name, 'Doe')
        self.assertEqual(self.patient.email, 'janedoe@example.org')
        self.assertEqual(self.patient.date_of_birth, datetime.date(2004, 3, 2))
        self.assertEqual(self.patient.gender, 'F')
        self.assertEqual(self.patient.location, 'GB')
        self.assertEqual(self.patient.ethnicity, 'BR')
        self.assertEqual(self.patient.language, 'en')
        self.assertEqual(self.patient.bio, "Hi, I'm Jane Doe")
        self.assertEqual(self.patient.condition, "Biliary atresia")
        self.assertEqual(self.patient.age_of_diagnosis, 2)

    def test_successful_profile_update_for_patient(self):
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
        self.assertEqual(self.patient.username, '@janedoe')
        self.assertEqual(self.patient.first_name, 'Jane')
        self.assertEqual(self.patient.last_name, 'Doe')
        self.assertEqual(self.patient.email, 'janedoe@example.org')
        self.assertEqual(self.patient.date_of_birth, datetime.date(1991, 1, 1)),
        self.assertEqual(self.patient.gender, 'F'),
        self.assertEqual(self.patient.location, 'US'),
        self.assertEqual(self.patient.ethnicity, 'RO'),
        self.assertEqual(self.patient.language, 'en'),
        self.assertEqual(self.patient.bio, "I am a test patient."),
        self.assertEqual(self.patient.condition, "Haemochromatosis"),
        self.assertEqual(self.patient.age_of_diagnosis, 21),
        self.assertEqual(self.patient.transplant, 'N')

    def test_successful_profile_update_for_parent(self):
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
        self.assertEqual(self.parent.username, '@johndoe')
        self.assertEqual(self.parent.first_name, 'John')
        self.assertEqual(self.parent.last_name, 'Doe')
        self.assertEqual(self.parent.email, 'johndoe@example.org')
        self.assertEqual(self.parent.date_of_birth, datetime.date(1990, 1, 1)),
        self.assertEqual(self.parent.gender, 'M'),
        self.assertEqual(self.parent.location, 'US'),
        self.assertEqual(self.parent.ethnicity, 'RO'),
        self.assertEqual(self.parent.language, 'en'),
        self.assertEqual(self.parent.bio, "I am a test parent."),
        self.assertEqual(self.parent.child_condition, "Haemochromatosis"),
        self.assertEqual(self.parent.child_age_of_diagnosis, 21),
        self.assertEqual(self.parent.child_transplant, 'N')

    def test_successful_profile_update_for_mentor(self):
        self.client.login(username=self.mentor.username, password='Password123')
        before_count = Mentor.objects.count()
        response = self.client.post(self.url, self.mentor_form_input, follow=True)
        after_count = Mentor.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.mentor.refresh_from_db()
        self.assertEqual(self.mentor.username, '@testmentor1')
        self.assertEqual(self.mentor.first_name, 'Test')
        self.assertEqual(self.mentor.last_name, 'Mentor')
        self.assertEqual(self.mentor.email, 'testmentor@example.org')
        self.assertEqual(self.mentor.date_of_birth, datetime.date(1991, 1, 1)),
        self.assertEqual(self.mentor.gender, 'M'),
        self.assertEqual(self.mentor.location, 'US'),
        self.assertEqual(self.mentor.ethnicity, 'RO'),
        self.assertEqual(self.mentor.language, 'en'),
        self.assertEqual(self.mentor.bio, 'I am a test mentor.'),
        self.assertEqual(self.mentor.condition, 'Haemochromatosis'),
        self.assertEqual(self.mentor.age_of_diagnosis, 21),
        self.assertEqual(self.mentor.referral_code, 'TEST123'),
        self.assertEqual(self.mentor.transplant, 'N')

    def test_post_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.patient_form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
