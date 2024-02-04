from django import template
from peer_support.models import Patient

register = template.Library()

@register.filter(name='is_patient')
def is_patient(user):
    return Patient.objects.filter(id=user.id).exists()