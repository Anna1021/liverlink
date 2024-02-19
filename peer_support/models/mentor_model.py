from django.db import models
from django.core.validators import MinValueValidator
from peer_support.models import User

class Mentor(User):
    """Model used for mentor authentication, and mentor related information."""
    
    mentor_condition = models.CharField(max_length=50, blank=True, null=True)
    mentor_age_of_diagnosis = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    referral_code = models.CharField(blank=False, null=False,max_length=10) 
    
    class Meta:
        verbose_name = 'Mentor'
        verbose_name_plural = 'Mentors'

