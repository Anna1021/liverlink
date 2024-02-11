from django import forms
from peer_support.forms import UserForm
from peer_support.models import Patient

class PatientForm(forms.ModelForm):
    """Form to update patient profiles."""

    class Meta:
        """Form options."""

        model = Patient
        fields = UserForm.Meta.fields + ['condition', 'age_of_diagnosis']
        widgets = UserForm.Meta.widgets