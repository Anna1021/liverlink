from django import forms
from django.core.validators import RegexValidator
from datetime import date

class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        cleaned_data = super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')
        return cleaned_data
    
class UserFormValidation(forms.ModelForm):

    def validate_dob(self, dob, user_type):
        """Check user is over 16 and under 25 years old."""

        today = date.today()
        if dob and (dob.year + 16, dob.month, dob.day) > (today.year, today.month, today.day):
            self.add_error('date_of_birth', 'You must be 16 years old to register.')
        if dob and (dob.year + 25, dob.month, dob.day) < (today.year, today.month, today.day) and user_type == "PT":
            self.add_error('date_of_birth', 'You must be less than 25 years old to register as a patient.')

    def clean(self):
        """Validate referral code and DOB."""
        cleaned_data = super().clean()
        referral_code = cleaned_data.get("referral_code")
        user_type = cleaned_data.get("user_type")
        dob = cleaned_data.get("date_of_birth")
        self.validate_referral_code(referral_code, user_type)
        self.validate_dob(dob, user_type)
        return cleaned_data

def apply_filter_if_needed(queryset, field_name, value):
    if value and value != "any":
        filter_kwargs = {field_name: value}
        return queryset.filter(**filter_kwargs)
    return queryset