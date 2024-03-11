from django.db import models
from django.core.validators import MinValueValidator
from peer_support.models import User

class Professional(User):
    """Model used for professional authentication, and professional related information."""
    
    expertise = models.CharField(max_length=50, blank=True, null=True)
    referral_code = models.CharField(blank=False, null=False,max_length=10) 
    
    class Meta:
        verbose_name = 'Professional'
        verbose_name_plural = 'Professionals'

