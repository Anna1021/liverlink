from django import template
from django.contrib.contenttypes.models import ContentType
from peer_support.models import Report
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.filter(name='is_object_reported_by_user')
def is_object_reported_by_user(object, user):
    content_type = ContentType.objects.get_for_model(object)
    return Report.objects.filter(content_type=content_type, object_id=object.id, reporter=user).exists()

@register.simple_tag
def display_reported_content(report):
    reported_object = report.content_object
    if not reported_object:
            return "Content not available"
    content_type = report.content_type
    if content_type.model == 'user':
        profile_url = reverse('profile', kwargs={'username': reported_object.username})
        return format_html('<a href="{}">{}</a>', profile_url, reported_object.username)
    elif content_type.model in ['question', 'response']:
        return reported_object.body
    elif content_type.model in ['message', 'post', 'postcomment']:
        return reported_object.content
    else:
        return "Content not available"
    
@register.filter(name='split')
def split_string(value, key):
    if hasattr(value, 'model'):
        value = value.model
    return value.split(key)