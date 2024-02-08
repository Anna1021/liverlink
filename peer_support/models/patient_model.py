from django.db import models
from django.core.validators import MinValueValidator
from peer_support.models import User
from .choices import GENDER_CHOICES, ETHNICITY_CHOICES, LANGUAGE_CHOICES, COUNTRY_CHOICES, HOSPITAL_CHOICES, CONDITION_CHOICES

class Patient(User):
    """Model used for patient authentication, and patient related information."""

    condition = models.CharField(max_length=100, blank=True, null=True)
    age_of_diagnosis = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
