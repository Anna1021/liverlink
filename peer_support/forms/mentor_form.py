from django import forms
from peer_support.forms import PatientForm
from peer_support.models import Mentor
from .form_choices import CONDITION_CHOICES

class MentorForm(forms.ModelForm):
    """Form to update mentor profiles."""

    condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    referral_code = forms.CharField(disabled=True, required=False)

    class Meta:
        """Form options."""

        model = Mentor
        fields = PatientForm.Meta.fields + ['referral_code']
        widgets = PatientForm.Meta.widgets