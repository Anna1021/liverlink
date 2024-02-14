from django import forms
#from django.contrib.auth import authenticate
from peer_support.models import Response

class NewResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']