from django import forms
from peer_support.models import User
from datetime import date

class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'date_of_birth', 'gender', 'location', 'hospital', 'ethnicity', 'language', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def validate_dob(self, dob):
        """Check user is over 13 years old."""

        today = date.today()
        if dob and (dob.year + 13, dob.month, dob.day) > (today.year, today.month, today.day):
            self.add_error('date_of_birth', 'You must be 13 years old to register.')

    def clean(self):
        """Validation of referral code and DOB."""
        
        cleaned_data = super().clean()
        dob = cleaned_data.get('date_of_birth')
        print(dob)
        self.validate_dob(dob)
        return cleaned_data
