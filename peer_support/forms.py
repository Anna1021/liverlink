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
            user = Patient.objects.create_user(**user_data)
        elif user_type == 'PR':
            user_data.update({
                'childs_condition': self.cleaned_data.get('childs_condition'),
                'childs_age_of_diagnosis': self.cleaned_data.get('childs_age_of_diagnosis'),
            })
            user = Parent.objects.create_user(**user_data)

        return user
    

class SortPeerForm(forms.Form):
    """Form enabling the sorting of users"""
    ALL_CHOICE = [('', 'None')]
    Username = forms.ChoiceField(choices=ALL_CHOICE+[('asc', 'Ascending'), ('desc', 'Descending')], required=False, label="Username")
    Age = forms.ChoiceField(choices=ALL_CHOICE+[('asc', 'Ascending'), ('desc', 'Descending')], required=False, label="Age")

    def clean(self):
        cleaned_data = super().clean()
        username_order = cleaned_data.get('Username')
        age_order = cleaned_data.get('Age')

        if username_order and age_order:
            self.add_error(None, 'Please choose only one sorting criterion: either Username or Age.')
        elif username_order == '' and age_order == '':
            pass
        return cleaned_data

    def sort_users(self, users):
        """Sorts users based on the selected criterion."""
        cleaned_data = self.cleaned_data 
        username_order = cleaned_data.get('Username')
        age_order = cleaned_data.get('Age')

        if username_order == 'asc':
            users = users.order_by('username')
        elif username_order == 'desc':
            users = users.order_by('-username')
        elif age_order == 'asc':
            users = users.order_by('date_of_birth')
        elif age_order == 'desc':
            users = users.order_by('-date_of_birth')

        return users


from django.utils import timezone
from datetime import timedelta
class FilterPeerForm(forms.Form):
    """Form enabling the filtering of users"""
    USER_TYPE_CHOICES=[('patient','Patient'), ('parent', 'Parent')]
    ALL_CHOICE = [('any', 'Any')]

    user_type=forms.MultipleChoiceField(choices=USER_TYPE_CHOICES,widget=forms.CheckboxSelectMultiple,required=False)
    min_age = forms.IntegerField(required=False, min_value=0, max_value=100)
    max_age = forms.IntegerField(required=False, min_value=0, max_value=100)
    gender = forms.MultipleChoiceField(choices=User.GENDER_CHOICES,widget=forms.CheckboxSelectMultiple,required=False)
    language = forms.ChoiceField(choices=ALL_CHOICE+User.LANGUAGE_CHOICES,required=False)
    ethnicity= forms.ChoiceField(choices=ALL_CHOICE+User.ETHNICITY_CHOICES,required=False)
    country = forms.ChoiceField(choices=ALL_CHOICE+User.COUNTRY_CHOICES,required=False)
    

    def __init__(self, *args, **kwargs):
        """Initialise query set with users tasks"""

        super(FilterPeerForm, self).__init__(*args, **kwargs)
        
    def filter_users(self, users):
        """Filters users based on critera provided"""
        user_type = self.cleaned_data.get('user_type')
        if user_type:
            combined_queryset = User.objects.none()
            if "patient" in user_type:
                patients = User.objects.filter(patient__isnull=False).distinct()
                combined_queryset = combined_queryset | patients
            if "parent" in user_type:
                parents = User.objects.filter(parent__isnull=False)
                combined_queryset = combined_queryset | parents
            
            users = users.distinct() & combined_queryset.distinct()

        genders = self.cleaned_data.get('gender')
        if genders:
            users = users.filter(gender__in=genders)

        current_date = timezone.now().date()
        min_age = self.cleaned_data.get('min_age')
        max_age = self.cleaned_data.get('max_age')

        if min_age is not None:
            min_birth_date = current_date - timedelta(days=365.25 * min_age)
            users = users.filter(date_of_birth__lte=min_birth_date)

        if max_age is not None:
            max_birth_date = current_date - timedelta(days=365.25 * (max_age + 1))
            users = users.filter(date_of_birth__gte=max_birth_date)

        language =self.cleaned_data.get('language')
        if language and "any" != language:
            users = users.filter(language=language)

        ethnicity =self.cleaned_data.get('ethnicity')
        if ethnicity and "any" != ethnicity:
            users = users.filter(ethnicity=ethnicity)
            
        country =self.cleaned_data.get('country')
        if country and "any" != country:
            users = users.filter(location=country)

        return users

class SearchPeerForm(forms.Form):
    """Form enabling the searching of users"""
    search = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

    def search_users(self, users):
        search_term = self.cleaned_data.get('search', '').strip()
        if search_term:
            users = users.filter(username__icontains=search_term)
        return users