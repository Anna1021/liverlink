from django import forms
from peer_support.forms import PatientForm
from peer_support.models import Mentor, Referral
from .form_choices import CONDITION_CHOICES, TRANSPLANT_CHOICES

class MentorForm(forms.ModelForm):
    """Form to update mentor profiles."""

    condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    referral_code = forms.CharField(disabled=True, required=False)
    transplant = forms.ChoiceField(choices=TRANSPLANT_CHOICES, required=False)

    class Meta:
        """Form options."""

        model = Mentor
        fields = PatientForm.Meta.fields + ['referral_code']
        widgets = PatientForm.Meta.widgets

    def validate_referral_code(self, referral_code):
        """Check mentors use an existing referral code."""

        try:
            Referral.objects.get(code=referral_code)
        except Referral.DoesNotExist:
            self.add_error('referral_code', "Please enter a valid referral code.")

    def clean(self):
        """Validation of referral code and DOB."""
        
        cleaned_data = super().clean()
        referral_code = cleaned_data.get('referral_code')
        self.validate_referral_code(referral_code)
        return cleaned_data