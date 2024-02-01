"""Forms for the peer_support app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User, Parent, Patient

class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

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

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""
        
        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    USER_TYPE_CHOICES = [
        ('PT', 'Patient'),
        ('PR', 'Parent'),
    ]
    
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

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
                'childs_condition': self.cleaned_data.get('childs_condition'),
                'childs_age_of_diagnosis': self.cleaned_data.get('childs_age_of_diagnosis'),
            })
            user = Parent.objects.create_user(**user_data)

        return user
    
class SortPeerForm(forms.Form):

    Username =  forms.ChoiceField(choices=[('asc', 'Ascending'), ('desc', 'Descending'), ('', 'Any')], required=False)

    def __init__(self, user, *args, **kwargs):
        """Initialise query set with users tasks"""

        super(SortPeerForm, self).__init__(*args, **kwargs)

    def sort_users(self, users):
        """Sorts users based on critera provided"""
        
        username_order = self.cleaned_data.get('Username')  
        if username_order == 'asc':
            users = users.order_by('username')
        elif username_order == 'desc':
            users = users.order_by('-username')

        return users

class FilterPeerForm(forms.Form):

    Email =  forms.ChoiceField(choices=[('a-n', 'A-N'), ('m-z', 'M-Z'),('', 'Any')], required=False)

    def __init__(self, user, *args, **kwargs):
        """Initialise query set with users tasks"""

        super(FilterPeerForm, self).__init__(*args, **kwargs)

    def filter_users(self, users):
        """Filters users based on critera provided"""
        
        email_filter = self.cleaned_data.get('Email')  
        if email_filter == 'a-n':
            users = User.objects.filter(email__regex=r'^[a-nA-N]')
        elif email_filter == 'm-z':
            users = User.objects.filter(email__regex=r'^[m-zM-Z]')

        return users
