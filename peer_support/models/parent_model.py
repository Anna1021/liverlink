from django.db import models
from django.core.validators import MinValueValidator
from peer_support.models import User

class Parent(User):
    """Model used for parent authentication, and parent related information."""
    
    child_condition = models.CharField(max_length=100, blank=True, null=True)
    child_age_of_diagnosis = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    child_transplant = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'