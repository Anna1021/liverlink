from django import forms
from peer_support.forms import UserForm
from peer_support.models import Patient
from .form_choices import CONDITION_CHOICES, TRANSPLANT_CHOICES

class PatientForm(forms.ModelForm):
    """Form to update patient profiles."""

    condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    age_of_diagnosis = forms.IntegerField(required=False, min_value=0)
    transplant = forms.ChoiceField(choices=TRANSPLANT_CHOICES, required=False)

    class Meta:
        """Form options."""

        model = Patient
        fields = UserForm.Meta.fields + ['condition', 'age_of_diagnosis']
        widgets = UserForm.Meta.widgets