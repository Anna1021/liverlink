from django import forms
from peer_support.forms import PatientForm, UserForm
from peer_support.models import Mentor
from .form_choices import CONDITION_CHOICES, TRANSPLANT_CHOICES


class MentorForm(UserForm, forms.ModelForm):
    """Form to update mentor profiles."""

    condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    transplant = forms.ChoiceField(choices=TRANSPLANT_CHOICES, required=False)

    class Meta:
        """Form options."""

        model = Mentor
        fields = PatientForm.Meta.fields
        widgets = PatientForm.Meta.widgets
