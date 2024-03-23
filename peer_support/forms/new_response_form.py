from django import forms
from peer_support.models import Response


class NewResponseForm(forms.ModelForm):
    """Form to reply to the questions"""

    class Meta:
        model = Response
        fields = ["body"]
