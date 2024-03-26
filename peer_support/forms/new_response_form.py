from django import forms
from peer_support.models import Response

class NewResponseForm(forms.ModelForm):
    """Form to reply to the questions"""
    
    body = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 8}),
        max_length=300 
    )
    class Meta:
        model = Response
        fields = ['body']