from django.db import models
from django.core.validators import MinValueValidator
from peer_support.models import User, Mentor

class Referral(models.Model):
    referrer = models.ForeignKey(Mentor, related_name='referrals_made', on_delete=models.CASCADE)
    referred = models.ForeignKey(Mentor, related_name='referrals_received', on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=20, unique=True)
    claimed = models.BooleanField(default=False)