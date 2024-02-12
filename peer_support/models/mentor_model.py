from django.db import models
from django.core.validators import MinValueValidator
from peer_support.models import User

class Mentor(User):
    """Model used for mentor authentication, and mentor related information."""
    
    mentor_condition = models.CharField(max_length=50, blank=True, null=True)
    mentor_age_of_diagnosis = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    # qualifications ??

    class Meta:
        verbose_name = 'Mentor'
        verbose_name_plural = 'Mentors'

class Referral(models.Model):
    referrer = models.ForeignKey(Mentor, related_name='referrals_made', on_delete=models.CASCADE)
    referred = models.ForeignKey(Mentor, related_name='referrals_received', on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=20, unique=True)
    claimed = models.BooleanField(default=False)
