from django import forms
#from django.contrib.auth import authenticate
from peer_support.models import Response

class NewReplyForm(forms.ModelForm):
    """Form to reply to the responses."""
    class Meta:
        model = Response
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'What are your thoughts?'
            })
        }