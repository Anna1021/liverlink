from django import forms
from peer_support.models import User
from django.utils import timezone
from datetime import timedelta
from peer_support.models.model_choices import GENDER_CHOICES, ETHNICITY_CHOICES, LANGUAGE_CHOICES, COUNTRY_CHOICES, HOSPITAL_CHOICES
from peer_support.forms.form_choices import CONDITION_CHOICES, USER_TYPE_CHOICES, TRANSPLANT_CHOICES
from .helpers import apply_filter_if_needed

class FilterUserForm(forms.Form):
    """Form enabling the filtering of users"""

    USER_TYPE_CHOICES = USER_TYPE_CHOICES[1:]
    ALL_CHOICE = [('any', 'Any')]
    user_type = forms.MultipleChoiceField(choices = USER_TYPE_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    min_age = forms.IntegerField(required = False, min_value=0)
    max_age = forms.IntegerField(required = False, min_value=0)
    gender = forms.MultipleChoiceField(choices = GENDER_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    language = forms.ChoiceField(choices = ALL_CHOICE+LANGUAGE_CHOICES, required=False)
    ethnicity = forms.ChoiceField(choices = ALL_CHOICE+ETHNICITY_CHOICES, required=False)
    country = forms.ChoiceField(choices = ALL_CHOICE+COUNTRY_CHOICES, required=False)
    hospital = forms.ChoiceField(choices = ALL_CHOICE+HOSPITAL_CHOICES, required=False)
    age_of_diagnosis_min = forms.IntegerField(required = False, min_value =0)
    age_of_diagnosis_max = forms.IntegerField(required=False, min_value=0)
    condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    child_age_of_diagnosis_min = forms.IntegerField(required=False, min_value=0)
    child_age_of_diagnosis_max = forms.IntegerField(required=False, min_value=0)
    child_condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    mentor_age_of_diagnosis_min = forms.IntegerField(required=False, min_value=0)
    mentor_age_of_diagnosis_max = forms.IntegerField(required=False, min_value=0)
    mentor_condition = forms.ChoiceField(choices=ALL_CHOICE+CONDITION_CHOICES, required=False)
    transplant = forms.ChoiceField(choices=TRANSPLANT_CHOICES, required=False)
    child_transplant = forms.ChoiceField(choices=TRANSPLANT_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        """Initialise query set with users tasks"""

        super(FilterUserForm, self).__init__(*args, **kwargs)

    def clean(self):
        """Validation of age fields"""

        cleaned_data = super().clean()
        age_ranges = [
            ('min_age', 'max_age', "Minimum age cannot be greater than maximum age."),
            ('age_of_diagnosis_min', 'age_of_diagnosis_max', "Minimum age of diagnosis cannot be greater than maximum age of diagnosis."),
            ('child_age_of_diagnosis_min', 'child_age_of_diagnosis_max', "Minimum child's age of diagnosis cannot be greater than maximum child's age of diagnosis."),
            ('mentor_age_of_diagnosis_min', 'mentor_age_of_diagnosis_max', "Minimum mentor's age of diagnosis cannot be greater than maximum mentor's age of diagnosis.")
        ]
        for min_key, max_key, error_message in age_ranges:
            min_value = cleaned_data.get(min_key)
            max_value = cleaned_data.get(max_key)
            if min_value is not None and max_value is not None and min_value > max_value:
                self.add_error(min_key, error_message)
                self.add_error(max_key, error_message.replace("Minimum", "Maximum").replace("cannot be greater than", "cannot be less than"))
        return cleaned_data
    
    def filter_users(self, users):
        """Filters users based on critera provided"""

        user_type = self.cleaned_data.get('user_type')
        if user_type:
            combined_queryset = self.filter_by_user_type(user_type)
            users = users.distinct() & combined_queryset.distinct()
        users = self.filter_by_gender(users)
        users = self.filter_by_age_range(users)
        filter_criteria = [
            ('language', self.cleaned_data.get('language')),
            ('ethnicity', self.cleaned_data.get('ethnicity')),
            ('location', self.cleaned_data.get('country')),
            ('hospital', self.cleaned_data.get('hospital')),
        ]
        for field_name, value in filter_criteria:
            users = apply_filter_if_needed(users, field_name, value)
        return users
    
    def filter_by_user_type(self,user_type):
        """Generates a list of users based on user type and user type specific fields"""

        combined_queryset = User.objects.none()
        if "PT" in user_type:
            patients = self.filter_by_patient_attributes()
            combined_queryset = combined_queryset | patients
        if "PR" in user_type:
            parents = self.filter_by_parent_attributes()
            combined_queryset = combined_queryset | parents
        if "MT" in user_type:
            mentors = self.filter_by_mentor_attributes()
            combined_queryset = combined_queryset | mentors
        return combined_queryset
    
    def filter_by_age_range(self, users):
        """Filters users based on age."""

        current_date = timezone.now().date()
        min_age = self.cleaned_data.get('min_age')
        max_age = self.cleaned_data.get('max_age')
        if min_age is not None:
            min_birth_date = current_date - timedelta(days=365.25 * min_age)
            users = users.filter(date_of_birth__lte=min_birth_date)
        if max_age is not None:
            max_birth_date = current_date - timedelta(days=365.25 * (max_age + 1))
            users = users.filter(date_of_birth__gte=max_birth_date)
        return users

    def filter_by_gender(self, users):
        """Filters users based on selected genders."""
        
        selected_genders = self.cleaned_data.get('gender')
        if selected_genders:
            users = users.filter(gender__in=selected_genders)
        return users
    
    def filter_by_patient_attributes(self):
        """Filters users based on patient attributes."""

        filter_criteria = {
            'age_of_diagnosis_min': 'patient__age_of_diagnosis__gte',
            'age_of_diagnosis_max': 'patient__age_of_diagnosis__lte',
            'condition': 'patient__condition__icontains',
            'transplant': 'patient__transplant__icontains',
        }
        patients = User.objects.filter(patient__isnull=False)
        return self.filter_by(patients,filter_criteria)
    
    def filter_by_parent_attributes(self):
        """Filters users based on parent attributes."""

        filter_criteria = {
            'child_age_of_diagnosis_min': 'parent__child_age_of_diagnosis__gte',
            'child_age_of_diagnosis_max': 'parent__child_age_of_diagnosis__lte',
            'child_condition': 'parent__child_condition__icontains',
            'child_transplant': 'parent__child_transplant__icontains',}
        parents = User.objects.filter(parent__isnull=False)
        return self.filter_by(parents,filter_criteria)
        
    def filter_by_mentor_attributes(self):
        """Filters users based on mentor attributes."""

        filter_criteria = {
            'mentor_age_of_diagnosis_min': 'mentor__age_of_diagnosis__gte',
            'mentor_age_of_diagnosis_max': 'mentor__age_of_diagnosis__lte',
            'mentor_condition': 'mentor__condition__icontains',
            'transplant': 'mentor__transplant__icontains',  }
        mentors = User.objects.filter(mentor__isnull=False)
        return self.filter_by(mentors,filter_criteria)
    
    def filter_by(self,users,criteria):
        """Filters users based on given criteria."""

        for criteria, query_filter in criteria.items():
            value = self.cleaned_data.get(criteria)
            if value and value != "any":
                users = users.filter(**{query_filter: value})
        return users