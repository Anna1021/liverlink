from django.db import models
from peer_support.models import Mentor

class Referral(models.Model):
    """Model used for referral related information."""
    referrer = models.ForeignKey(Mentor, related_name='referrals_made', on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True)