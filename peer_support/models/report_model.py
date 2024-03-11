from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from peer_support.models import User
from .model_choices import REPORT_CHOICES

class Report(models.Model):
    """Model used for reporting objects to moderators (staff)"""
    reporter = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50,choices=REPORT_CHOICES)
    reported_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

