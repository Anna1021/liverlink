"""Unit tests for the Patient model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from peer_support.models import Patient

class PatientModelTestCase(TestCase):
    """Unit tests for the Patient model."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_patient.json',
        'peer_support/tests/fixtures/other_patients.json'
    ]

    def setUp(self):
        self.patient = Patient.objects.get(username='@johndoe')

    def test_valid_patient(self):
        self._assert_patient_is_valid()

    def test_condition_can_be_blank(self):
        self.patient.condition = ''
        self._assert_patient_is_valid()

    def test_condition_need_not_be_unique(self):
        second_patient = Patient.objects.get(username='@janedoe')
        self.patient.condition = second_patient.condition
        self._assert_patient_is_valid()

    def test_condition_can_be_100_characters_long(self):
        self.patient.condition = 'x' * 100
        self._assert_patient_is_valid()

    def test_condition_cannot_be_over_100_characters_long(self):
        self.patient.condition = 'x' * 101
        self._assert_patient_is_invalid()

    
    def test_age_of_diagnosis_can_be_blank(self):
        self.patient.age_of_diagnosis = None
        self._assert_patient_is_valid()

    def test_age_of_diagnosis_need_not_be_unique(self):
        second_patient = Patient.objects.get(username='@janedoe')
        self.patient.age_of_diagnosis = second_patient.age_of_diagnosis
        self._assert_patient_is_valid()

    def test_age_of_diagnosis_cannot_be_negative(self):
        self.patient.age_of_diagnosis = -1
        self._assert_patient_is_invalid()


    def _assert_patient_is_valid(self):
        try:
            self.patient.full_clean()
        except (ValidationError):
            self.fail('Test patient should be valid')

    def _assert_patient_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.patient.full_clean()

    