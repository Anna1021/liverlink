from django import forms
from peer_support.models import User, Parent, Patient, Mentor, Professional, Referral
from .helpers import NewPasswordMixin
from datetime import date
from .form_choices import USER_TYPE_CHOICES, CONDITION_CHOICES, TRANSPLANT_CHOICES

class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""
    
    user_type = forms.ChoiceField(initial='', choices=USER_TYPE_CHOICES, required=True)
    referral_code = forms.CharField(required=False, max_length=10, initial='')

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'date_of_birth'] 
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self):
        """Create a new user."""

        user_data = self.get_user_data()
        user_type = self.cleaned_data.get('user_type')
        if user_type == 'PT':
            user = self.create_patient(user_data)
        elif user_type == 'PR':
            user = self.create_parent(user_data)
        elif user_type == 'MT':
            user = self.create_mentor(user_data)
        else:
            user = self.create_professional(user_data)
        return user

    def get_user_data(self):
        """Get the common user data."""

        return {
            'username': self.cleaned_data.get('username'),
            'first_name': self.cleaned_data.get('first_name'),
            'last_name': self.cleaned_data.get('last_name'),
            'email': self.cleaned_data.get('email'),
            'password': self.cleaned_data.get('new_password'),
            'date_of_birth': self.cleaned_data.get('date_of_birth'),
        }

    def create_patient(self, user_data):
        """Create a new Patient user."""

        return Patient.objects.create_user(**user_data)

    def create_parent(self, user_data):
        """Create a new Parent user."""

        return Parent.objects.create_user(**user_data)

    def create_mentor(self, user_data):
        """Create a new Mentor user."""

        user_data.update({
            'referral_code': self.cleaned_data.get('referral_code'),
        })

        return Mentor.objects.create_user(**user_data)
    
    def create_professional(self, user_data):
        """Create a new Professional user."""

        user_data.update({
            'referral_code': self.cleaned_data.get('referral_code'),
        })
        
        return Professional.objects.create_user(**user_data)
    
    def validate_referral_code(self, referral_code, user_type):
        """Check mentors and professionals use an existing referral code."""

        if user_type == 'MT' or user_type == 'PF':
            try:
                Referral.objects.get(code=referral_code)
            except Referral.DoesNotExist:
                self.add_error('referral_code', "Please enter a valid referral code.")

    def validate_dob(self, dob):
        """Check user is over 16 years old."""

        today = date.today()
        if dob and (dob.year + 16, dob.month, dob.day) > (today.year, today.month, today.day):
            self.add_error('date_of_birth', 'You must be 16 years old to register.')

    def clean(self):
        """Validation of referral code and DOB."""
        
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        referral_code = cleaned_data.get('referral_code')
        dob = cleaned_data.get('date_of_birth')
        self.validate_referral_code(referral_code, user_type)
        self.validate_dob(dob)
        return cleaned_data