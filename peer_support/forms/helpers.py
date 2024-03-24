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
    
def validate_min_age(dob):
    """Check user is over 16 years old."""

    today = date.today()
    if dob and (dob.year + 16, dob.month, dob.day) > (today.year, today.month, today.day):
        raise forms.ValidationError('You must be 16 years old.')
    
def validate_max_age(dob, user_type):
    """Check user is under 25 years old."""

    today = date.today()
    if dob and (dob.year + 25, dob.month, dob.day) < (today.year, today.month, today.day) and user_type == "PT":
        raise forms.ValidationError('You must be less than 25 years old to be a patient.')
    
def apply_filter_if_needed(queryset, field_name, value):
    if value and value != "any":
        filter_kwargs = {field_name: value}
        return queryset.filter(**filter_kwargs)
    return queryset