from django import forms
from peer_support.forms import UserForm
from peer_support.models import Patient
from .form_choices import CONDITION_CHOICES, TRANSPLANT_CHOICES
from datetime import date

class PatientForm(UserForm, forms.ModelForm):
    """Form to update patient profiles."""

    condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    age_of_diagnosis = forms.IntegerField(required=False, min_value=0)
    transplant = forms.ChoiceField(choices=TRANSPLANT_CHOICES, required=False)

    class Meta:
        """Form options."""

        model = Patient
        fields = UserForm.Meta.fields + ['condition', 'age_of_diagnosis', 'transplant']
        widgets = UserForm.Meta.widgets

    def validate_max_dob(self, dob):
        """Check user is under 25 years old."""

        today = date.today()
        if dob and (dob.year + 25, dob.month, dob.day) < (today.year, today.month, today.day):
            self.add_error('date_of_birth', 'You must be less than 25 years old to register as a patient.')

    def clean(self):
        """Validation of DOB."""
        
        cleaned_data = super().clean()
        dob = cleaned_data.get('date_of_birth')
        self.validate_max_dob(dob)
        return cleaned_data