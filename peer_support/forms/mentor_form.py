from django import forms
from peer_support.forms import PatientForm
from peer_support.models import Mentor
from .form_choices import CONDITION_CHOICES, TRANSPLANT_CHOICES
from .helpers import validate_min_age


class MentorForm(forms.ModelForm):
    """Form to update mentor profiles."""

    condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    referral_code = forms.CharField(disabled=True, required=False)
    transplant = forms.ChoiceField(choices=TRANSPLANT_CHOICES, required=False)

    class Meta:
        """Form options."""

        model = Mentor
        fields = PatientForm.Meta.fields + ["referral_code"]
        widgets = PatientForm.Meta.widgets

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get("date_of_birth")
        validate_min_age(dob)
        return dob
