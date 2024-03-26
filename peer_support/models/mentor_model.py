from django.db import models
from django.core.validators import MinValueValidator
from peer_support.models import User

class Mentor(User):
    """Model used for mentor authentication, and mentor related information."""
    
    condition = models.CharField(max_length=100, blank=True, null=True)
    age_of_diagnosis = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    transplant = models.CharField(max_length=50, blank=True, null=True)
    """The referral code is that which referred the user to the platform."""
    referral_code = models.CharField(blank=False, null=False, max_length=10)

    class Meta:
        verbose_name = 'Mentor'
        verbose_name_plural = 'Mentors'
