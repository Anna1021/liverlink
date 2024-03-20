from django import template
from django.contrib.contenttypes.models import ContentType
from peer_support.models import Report

register = template.Library()

@register.filter(name='is_comment_reported_by_user')
def is_comment_reported_by_user(comment, user):
    content_type = ContentType.objects.get_for_model(comment)
    return Report.objects.filter(content_type=content_type, object_id=comment.id, reporter=user).exists()
