from django import forms
from peer_support.forms import PatientForm
from peer_support.models import Mentor

class MentorForm(forms.ModelForm):
    """Form to update mentor profiles."""

    referral_code = forms.CharField(disabled=True)
    

    class Meta:
        """Form options."""

        model = Mentor
        fields = PatientForm.Meta.fields + ['referral_code']
        widgets = PatientForm.Meta.widgets