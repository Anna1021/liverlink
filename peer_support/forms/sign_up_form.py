from django import forms
from peer_support.models import User, Parent, Patient, Mentor
from .helpers import NewPasswordMixin
from .form_choices import USER_TYPE_CHOICES, CONDITION_CHOICES

class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    USER_TYPE_CHOICES = [
        ('', '---------'),
        ('PT', 'Patient'),
        ('PR', 'Parent'),
        ('MT', 'Mentor'),
    ]
    
    user_type = forms.ChoiceField(initial='', choices=USER_TYPE_CHOICES, required=True)
    condition = forms.CharField(required=False)
    age_of_diagnosis = forms.IntegerField(required=False)
    child_condition = forms.CharField(required=False)
    child_age_of_diagnosis = forms.IntegerField(required=False)
    mentor_condition = forms.CharField(required=False)
    mentor_age_of_diagnosis = forms.IntegerField(required=False)
    referral_code = forms.CharField(required=True, max_length=10)
    

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'date_of_birth', 'gender', 'location', 'ethnicity', 'language', 'bio']
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
            'ethnicity': self.cleaned_data.get('ethnicity'),
            'language': self.cleaned_data.get('language'),
            'bio': self.cleaned_data.get('bio'),
        }

        user_type = self.cleaned_data.get('user_type')
        if user_type == 'PT':
            user_data.update({
                'condition': self.cleaned_data.get('condition'),
                'age_of_diagnosis': self.cleaned_data.get('age_of_diagnosis'),
            })
            print(user_data)
            user = Patient.objects.create_user(**user_data)
        elif user_type == 'PR':
            user_data.update({
                'child_condition': self.cleaned_data.get('child_condition'),
                'child_age_of_diagnosis': self.cleaned_data.get('child_age_of_diagnosis'),
            })
            user = Parent.objects.create_user(**user_data)
        elif user_type == 'MT':
            user_data.update({
                'mentor_condition': self.cleaned_data.get('mentor_condition'),
                'mentor_age_of_diagnosis': self.cleaned_data.get('mentor_age_of_diagnosis'),
                'referral_code': self.cleaned_data.get('referral_code')
            })
            print(user_data)
            user = Mentor.objects.create_user(**user_data)

        return user