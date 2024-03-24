from django import forms
from peer_support.forms import UserForm
from peer_support.models import Patient
from .form_choices import CONDITION_CHOICES, TRANSPLANT_CHOICES
from .helpers import validate_min_age, validate_max_age

class PatientForm(forms.ModelForm):
    """Form to update patient profiles."""

    condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    age_of_diagnosis = forms.IntegerField(required=False, min_value=0)
    transplant = forms.ChoiceField(choices=TRANSPLANT_CHOICES, required=False)

    class Meta:
        """Form options."""

        model = Patient
        fields = UserForm.Meta.fields + ['condition', 'age_of_diagnosis', 'transplant']
        widgets = UserForm.Meta.widgets

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        validate_min_age(dob)
        validate_max_age(dob, "PT")
        return dob
