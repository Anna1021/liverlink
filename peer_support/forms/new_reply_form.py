from django import forms
from peer_support.models import Response
class NewReplyForm(forms.ModelForm):
    """Form to reply to the responses."""
    
    body = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        max_length=200 
    )
    class Meta:
        model = Response
        fields = ['body']