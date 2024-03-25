"""Tests for the profile update view."""
import datetime
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from peer_support.forms import PatientForm, ParentForm, MentorForm, UserForm, ProfessionalForm
from peer_support.models import Patient, Parent, Mentor, User, Professional, Referral
from peer_support.tests.helpers import reverse_with_next
from peer_support.views.helpers import get_referral_code

class ProfileUpdateViewTestCase(TestCase):
    """Test suite for the profile update view."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_mentor.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/other_patients.json',
        'peer_support/tests/fixtures/other_parents.json',
        'peer_support/tests/fixtures/other_professionals.json',
        'peer_support/tests/fixtures/default_user_profile.json',
        'peer_support/tests/fixtures/other_user_profiles.json',
        'peer_support/tests/fixtures/default_admin.json'
    ]

    def setUp(self):
        self.parent = Parent.objects.get(username='@alexsmith')
        self.admin = User.objects.get(username='@admin')
        self.patient = Patient.objects.get(username='@janedoe')
        self.mentor = Mentor.objects.get(username='@johndoe')
        self.professional = Professional.objects.get(username='@hazelsmith')
        self.url = reverse('settings')
        self.user_form_input = {
            'first_name': 'Admin',
            'last_name': 'Test',
            'username': '@admin',
            'email': 'admin_2@example.org',
            'date_of_birth': '1990-01-01',
            'gender': 'N',
            'location': 'US',
            'ethnicity': 'RO',
            'language': 'en',
            'bio': 'I am a test admin.',
        }
        self.parent_form_input = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': '@alexsmith',
            'email': 'alexsmith@example.org',
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
            'date_of_birth': '2002-01-01',
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
        }
        self.professional_form_input = {
            'first_name': 'Test',
            'last_name': 'Professional',
            'username': '@testprofessional1',
            'email': 'testprofessional@example.org',
            'date_of_birth': '1991-01-01',
            'gender': 'M',
            'location': 'US',
            'ethnicity': 'RO',
            'language': 'en',
            'bio': 'I am a test professional.',
            'expertise': 'Haemochromatosis',
            'referral_code': '9C274FF391',
        }

    def test_profile_url(self):
        self.assertEqual(self.url, '/settings/')

    def test_get_user_form_when_current_user_is_user(self):
        self.client.force_login(self.admin)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'settings.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))

    def test_get_patient_form_when_current_user_is_patient(self):
        self.client.force_login(self.patient)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'settings.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PatientForm))

    def test_get_parent_form_when_current_user_is_parent(self):
        self.client.force_login(self.parent)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'settings.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ParentForm))  

    def test_get_mentor_form_when_current_user_is_mentor(self):
        self.client.force_login(self.mentor)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'settings.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, MentorForm))

    def test_get_professional_form_when_current_user_is_professional(self):
        self.client.force_login(self.professional)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'settings.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ProfessionalForm))

    def test_referral_code_is_none_when_current_user_is_not_professional(self):
        for user in [self.admin, self.patient, self.parent, self.mentor]:
            self.client.force_login(user)
            response = self.client.get(self.url)
            referral_code = response.context['referral_code']
            self.assertIsNone(referral_code)

    def test_referral_code_when_current_user_is_professional(self):
        Referral.objects.create(referrer=self.professional, code=self.professional.referral_code)
        self.client.force_login(self.professional)
        response = self.client.get(self.url)
        referral_code = response.context['referral_code']
        self.assertEqual(referral_code, self.professional.referral_code)

    def test_get_profile(self):
        self.client.force_login(self.patient)
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

    def test_unsuccessful_profile_update_for_user(self):
        self.client.force_login(self.admin)
        self.user_form_input['username'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.user_form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertTrue(form.is_bound)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.username, '@admin')
        self.assertEqual(self.admin.first_name, 'Admin')
        self.assertEqual(self.admin.last_name, 'User')
        self.assertEqual(self.admin.email, 'admin@example.com')
        self.assertEqual(self.admin.date_of_birth, datetime.date(1990, 1, 1)),
        self.assertEqual(self.admin.gender, 'N'),
        self.assertEqual(self.admin.location, 'US')

    def test_unsuccessful_profile_update_for_patient(self):
        self.client.force_login(self.patient)
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
        self.client.force_login(self.parent)
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
        self.assertEqual(self.parent.username, '@alexsmith')
        self.assertEqual(self.parent.first_name, 'Alex')
        self.assertEqual(self.parent.last_name, 'Smith')
        self.assertEqual(self.parent.email, 'alexsmith@example.com')
        self.assertEqual(self.parent.date_of_birth, datetime.date(1978, 8, 12))
        self.assertEqual(self.parent.gender, 'M')
        self.assertEqual(self.parent.location, 'US')
        self.assertEqual(self.parent.ethnicity, 'OW')
        self.assertEqual(self.parent.bio, "Hi, I'm Alex Smith, an avid reader and tech enthusiast.")
        self.assertEqual(self.parent.child_condition, "Biliary atresia")
        self.assertEqual(self.parent.child_age_of_diagnosis, 2)

    def test_unsuccessful_profile_update_for_mentor(self):
        self.client.force_login(self.mentor)
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
        self.assertEqual(self.mentor.username, '@johndoe')
        self.assertEqual(self.mentor.first_name, 'John')
        self.assertEqual(self.mentor.last_name, 'Doe')
        self.assertEqual(self.mentor.email, 'johndoe@example.org')
        self.assertEqual(self.mentor.date_of_birth, datetime.date(2001, 1, 1))
        self.assertEqual(self.mentor.gender, 'M')
        self.assertEqual(self.mentor.location, 'GB')
        self.assertEqual(self.mentor.ethnicity, 'BR')
        self.assertEqual(self.mentor.language, 'en')
        self.assertEqual(self.mentor.bio, "I'm a test user")
        self.assertEqual(self.mentor.condition, 'Cirrhosis')
        self.assertEqual(self.mentor.age_of_diagnosis, 13) 
        self.assertEqual(self.mentor.transplant, 'Y') 
        self.assertEqual(self.mentor.referral_code, '9C274FF391') 

    def test_unsuccessful_profile_update_for_professional(self):
        self.client.force_login(self.professional)
        self.professional_form_input['username'] = 'BAD_USERNAME'
        before_count = Professional.objects.count()
        response = self.client.post(self.url, self.professional_form_input)
        after_count = Professional.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')
        form = response.context['form']
        self.assertTrue(form.is_bound)
        self.professional.refresh_from_db()
        self.assertEqual(self.professional.username, '@hazelsmith')
        self.assertEqual(self.professional.first_name, 'Hazel')
        self.assertEqual(self.professional.last_name, 'Smith')
        self.assertEqual(self.professional.email, 'hazelsmith@example.com')
        self.assertEqual(self.professional.date_of_birth, datetime.date(1981, 1, 3))
        self.assertEqual(self.professional.gender, 'F')
        self.assertEqual(self.professional.location, 'US')
        self.assertEqual(self.professional.ethnicity, 'AS')
        self.assertEqual(self.professional.bio, "I'm a professional therapist and I'm here to help you.")
        self.assertEqual(self.professional.expertise, 'Biliary atresia')
        self.assertEqual(self.professional.referral_code, '9C274FF391') 

    def test_unsuccessful_profile_update_due_to_duplicate_username(self):
        self.client.force_login(self.patient)
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

    def test_successful_profile_update_for_user(self):
        self.client.force_login(self.admin)
        before_count = User.objects.count()
        response = self.client.post(self.url, self.user_form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.username, '@admin')
        self.assertEqual(self.admin.first_name, 'Admin')
        self.assertEqual(self.admin.last_name, 'Test')
        self.assertEqual(self.admin.email, 'admin_2@example.org')
        self.assertEqual(self.admin.date_of_birth, datetime.date(1990, 1, 1)),
        self.assertEqual(self.admin.gender, 'N'),
        self.assertEqual(self.admin.location, 'US'),
        self.assertEqual(self.admin.ethnicity, 'RO'),
        self.assertEqual(self.admin.language, 'en'),
        self.assertEqual(self.admin.bio, "I am a test admin.")

    def test_successful_profile_update_for_patient(self):
        self.client.force_login(self.patient)
        before_count = Patient.objects.count()
        response = self.client.post(self.url, self.patient_form_input, follow=True)
        after_count = Patient.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.username, '@janedoe')
        self.assertEqual(self.patient.first_name, 'Jane')
        self.assertEqual(self.patient.last_name, 'Doe')
        self.assertEqual(self.patient.email, 'janedoe@example.org')
        self.assertEqual(self.patient.date_of_birth, datetime.date(2002, 1, 1)),
        self.assertEqual(self.patient.gender, 'F'),
        self.assertEqual(self.patient.location, 'US'),
        self.assertEqual(self.patient.ethnicity, 'RO'),
        self.assertEqual(self.patient.language, 'en'),
        self.assertEqual(self.patient.bio, "I am a test patient."),
        self.assertEqual(self.patient.condition, "Haemochromatosis"),
        self.assertEqual(self.patient.age_of_diagnosis, 21),
        self.assertEqual(self.patient.transplant, 'N')

    def test_successful_profile_update_for_parent(self):
        self.client.force_login(self.parent)
        before_count = Parent.objects.count()
        response = self.client.post(self.url, self.parent_form_input, follow=True)
        after_count = Parent.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.parent.refresh_from_db()
        self.assertEqual(self.parent.username, '@alexsmith')
        self.assertEqual(self.parent.first_name, 'John')
        self.assertEqual(self.parent.last_name, 'Doe')
        self.assertEqual(self.parent.email, 'alexsmith@example.org')
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
        self.client.force_login(self.mentor)
        before_count = Mentor.objects.count()
        response = self.client.post(self.url, self.mentor_form_input, follow=True)
        after_count = Mentor.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
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
        self.assertEqual(self.mentor.referral_code, '9C274FF391'),
        self.assertEqual(self.mentor.transplant, 'N')

    def test_successful_profile_update_for_professional(self):
        self.client.force_login(self.professional)
        before_count = Professional.objects.count()
        response = self.client.post(self.url, self.professional_form_input, follow=True)
        after_count = Professional.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.professional.refresh_from_db()
        self.assertEqual(self.professional.username, '@testprofessional1')
        self.assertEqual(self.professional.first_name, 'Test')
        self.assertEqual(self.professional.last_name, 'Professional')
        self.assertEqual(self.professional.email, 'testprofessional@example.org')
        self.assertEqual(self.professional.date_of_birth, datetime.date(1991, 1, 1)),
        self.assertEqual(self.professional.gender, 'M'),
        self.assertEqual(self.professional.location, 'US'),
        self.assertEqual(self.professional.ethnicity, 'RO'),
        self.assertEqual(self.professional.language, 'en'),
        self.assertEqual(self.professional.bio, 'I am a test professional.'),
        self.assertEqual(self.professional.expertise, 'Haemochromatosis'),
        self.assertEqual(self.professional.referral_code, '9C274FF391'),

    def test_post_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.patient_form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)