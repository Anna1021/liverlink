from django import forms
from peer_support.models import User, Parent, Patient, Mentor, Referral
from .helpers import NewPasswordMixin
from datetime import date
from .form_choices import USER_TYPE_CHOICES, CONDITION_CHOICES, TRANSPLANT_CHOICES

class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""
    
    user_type = forms.ChoiceField(initial='', choices=USER_TYPE_CHOICES, required=True)
    condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    age_of_diagnosis = forms.IntegerField(required=False, min_value=0)
    child_condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    child_age_of_diagnosis = forms.IntegerField(required=False, min_value=0)
    referral_code = forms.CharField(required=False, max_length=10, initial='')
    transplant = forms.ChoiceField(choices=TRANSPLANT_CHOICES, required=False)
    child_transplant = forms.ChoiceField(choices=TRANSPLANT_CHOICES, required=False)

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'date_of_birth', 'gender', 'location', 'hospital', 'ethnicity', 'language', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self):
        """Create a new user."""
        user_data = {
            'username': self.cleaned_data.get('username'),
            'first_name': self.cleaned_data.get('first_name'),
            'last_name': self.cleaned_data.get('last_name'),
            'email': self.cleaned_data.get('email'),
            'password': self.cleaned_data.get('new_password'),
            'date_of_birth': self.cleaned_data.get('date_of_birth'),
            'gender': self.cleaned_data.get('gender'),
            'location': self.cleaned_data.get('location'),
            'hospital': self.cleaned_data.get('hospital'),
            'ethnicity': self.cleaned_data.get('ethnicity'),
            'language': self.cleaned_data.get('language'),
            'bio': self.cleaned_data.get('bio'),
        }
        user_type = self.cleaned_data.get('user_type')
        if user_type == 'PT':
            user_data.update({
                'condition': self.cleaned_data.get('condition'),
                'age_of_diagnosis': self.cleaned_data.get('age_of_diagnosis'),
                'transplant': self.cleaned_data.get('transplant'),
            })
            user = Patient.objects.create_user(**user_data)
        elif user_type == 'PR':
            user_data.update({
                'child_condition': self.cleaned_data.get('child_condition'),
                'child_age_of_diagnosis': self.cleaned_data.get('child_age_of_diagnosis'),
                'child_transplant': self.cleaned_data.get('child_transplant'),
            })
            user = Parent.objects.create_user(**user_data)
        else:
            user_data.update({
                'condition': self.cleaned_data.get('condition'),
                'age_of_diagnosis': self.cleaned_data.get('age_of_diagnosis'),
                'transplant': self.cleaned_data.get('transplant'),
                'referral_code': self.cleaned_data.get('referral_code')
            })
            user = Mentor.objects.create_user(**user_data)

        return user

    def clean(self):
        """Validation of referral code and DOB."""
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        referral_code = cleaned_data.get('referral_code')
        if user_type == 'MT':
            try:
                Referral.objects.get(code=referral_code)
            except Referral.DoesNotExist:
                self.add_error('referral_code', "Please enter a valid referral code.")
        dob = self.cleaned_data.get('date_of_birth')
        today = date.today()
        if dob is not None and (dob.year + 13, dob.month, dob.day) > (today.year, today.month, today.day):
            self.add_error('date_of_birth', 'You must be 13 years old to register.')
        return cleaned_data
