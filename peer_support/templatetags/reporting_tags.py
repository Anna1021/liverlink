from django import template
from django.contrib.contenttypes.models import ContentType
from peer_support.models import Report

register = template.Library()

@register.filter(name='is_object_reported_by_user')
def is_object_reported_by_user(object, user):
    content_type = ContentType.objects.get_for_model(object)
    return Report.objects.filter(content_type=content_type, object_id=object.id, reporter=user).exists()
