from django import forms
from peer_support.models import User
from django.utils import timezone
from datetime import timedelta
from peer_support.models.model_choices import GENDER_CHOICES, ETHNICITY_CHOICES, LANGUAGE_CHOICES, COUNTRY_CHOICES, HOSPITAL_CHOICES
from peer_support.forms.form_choices import CONDITION_CHOICES, USER_TYPE_CHOICES, TRANSPLANT_CHOICES

class FilterPeerForm(forms.Form):
    """Form enabling the filtering of users"""
    USER_TYPE_CHOICES = USER_TYPE_CHOICES[1:]
    ALL_CHOICE = [('any', 'Any')]
    user_type=forms.MultipleChoiceField(choices=USER_TYPE_CHOICES,widget=forms.CheckboxSelectMultiple,required=False)
    min_age = forms.IntegerField(required=False, min_value=0)
    max_age = forms.IntegerField(required=False, min_value=0)
    gender = forms.MultipleChoiceField(choices=GENDER_CHOICES,widget=forms.CheckboxSelectMultiple,required=False)
    language = forms.ChoiceField(choices=ALL_CHOICE+LANGUAGE_CHOICES,required=False)
    ethnicity= forms.ChoiceField(choices=ALL_CHOICE+ETHNICITY_CHOICES,required=False)
    country = forms.ChoiceField(choices=ALL_CHOICE+COUNTRY_CHOICES,required=False)
    hospital = forms.ChoiceField(choices=ALL_CHOICE+HOSPITAL_CHOICES,required=False)
    age_of_diagnosis_min = forms.IntegerField(required=False, min_value=0)
    age_of_diagnosis_max = forms.IntegerField(required=False, min_value=0)
    condition=forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    child_age_of_diagnosis_min = forms.IntegerField(required=False, min_value=0)
    child_age_of_diagnosis_max = forms.IntegerField(required=False, min_value=0)
    child_condition=forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    mentor_age_of_diagnosis_min = forms.IntegerField(required=False, min_value=0)
    mentor_age_of_diagnosis_max = forms.IntegerField(required=False, min_value=0)
    mentor_condition=forms.ChoiceField(choices=ALL_CHOICE+CONDITION_CHOICES, required=False)
    transplant=forms.ChoiceField(choices=TRANSPLANT_CHOICES, required=False)
    child_transplant=forms.ChoiceField(choices=TRANSPLANT_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        """Initialise query set with users tasks"""
        super(FilterPeerForm, self).__init__(*args, **kwargs)

    def clean(self):
        """Validation of age fields"""
        cleaned_data = super().clean()
        min_age = cleaned_data.get('min_age')
        max_age = cleaned_data.get('max_age')
        if min_age is not None and max_age is not None and min_age > max_age:
            self.add_error('min_age', "Minimum age cannot be greater than maximum age.")
            self.add_error('max_age', "Maximum age cannot be less than minimum age.")
        age_of_diagnosis_min = cleaned_data.get('age_of_diagnosis_min')
        age_of_diagnosis_max = cleaned_data.get('age_of_diagnosis_max')
        if age_of_diagnosis_min is not None and age_of_diagnosis_max is not None and age_of_diagnosis_min > age_of_diagnosis_max:
            self.add_error('age_of_diagnosis_min', "Minimum age of diagnosis cannot be greater than maximum age of diagnosis.")
            self.add_error('age_of_diagnosis_max', "Maximum age of diagnosis cannot be less than minimum age of diagnosis.")
        child_age_of_diagnosis_min = cleaned_data.get('child_age_of_diagnosis_min')
        child_age_of_diagnosis_max = cleaned_data.get('child_age_of_diagnosis_max')
        if child_age_of_diagnosis_min is not None and child_age_of_diagnosis_max is not None and child_age_of_diagnosis_min > child_age_of_diagnosis_max:
            self.add_error('child_age_of_diagnosis_min', "Minimum child's age of diagnosis cannot be greater than maximum child's age of diagnosis.")
            self.add_error('child_age_of_diagnosis_max', "Maximum child's age of diagnosis cannot be less than minimum child's age of diagnosis.")
        mentor_age_of_diagnosis_min = cleaned_data.get('mentor_age_of_diagnosis_min')
        mentor_age_of_diagnosis_max = cleaned_data.get('mentor_age_of_diagnosis_max')
        if mentor_age_of_diagnosis_min is not None and mentor_age_of_diagnosis_max is not None and mentor_age_of_diagnosis_min > mentor_age_of_diagnosis_max:
            self.add_error('mentor_age_of_diagnosis_min', "Minimum mentor's age of diagnosis cannot be greater than maximum mentor's age of diagnosis.")
            self.add_error('mentor_age_of_diagnosis_max', "Maximum mentor's age of diagnosis cannot be less than minimum mentor's age of diagnosis.")
        return cleaned_data
    
    def filter_by_patient(self):
        age_of_diagnosis_min = self.cleaned_data.get('age_of_diagnosis_min')
        age_of_diagnosis_max = self.cleaned_data.get('age_of_diagnosis_max')
        condition =self.cleaned_data.get('condition')
        transplant=self.cleaned_data.get('transplant')
        patients = User.objects.filter(patient__isnull=False)
        if age_of_diagnosis_min is not None:
            patients = patients.filter(patient__age_of_diagnosis__gte=age_of_diagnosis_min)
        if age_of_diagnosis_max is not None:
            patients = patients.filter(patient__age_of_diagnosis__lte=age_of_diagnosis_max)
        if condition and "any" != condition:
            patients = patients.filter(patient__condition__icontains=condition)
        if transplant and "any" != transplant:
            patients = patients.filter(patient__transplant__icontains=transplant)
        return patients
    
    def filter_by_parent(self):
        child_age_of_diagnosis_min = self.cleaned_data.get('child_age_of_diagnosis_min')
        child_age_of_diagnosis_max = self.cleaned_data.get('child_age_of_diagnosis_max')
        child_condition =self.cleaned_data.get('child_condition')
        child_transplant=self.cleaned_data.get('child_transplant')
        parents = User.objects.filter(parent__isnull=False)
        if child_age_of_diagnosis_min is not None:
            parents = parents.filter(parent__child_age_of_diagnosis__gte=child_age_of_diagnosis_min)
        if child_age_of_diagnosis_max is not None:
            parents = parents.filter(parent__child_age_of_diagnosis__lte=child_age_of_diagnosis_max)
        if child_condition and "any" != child_condition:
            parents = parents.filter(parent__child_condition__icontains=child_condition)
        if child_transplant and "any" != child_transplant:
            parents = parents.filter(parent__child_transplant__icontains=child_transplant)
        return parents
        
    def filter_by_mentor(self):
        mentor_age_of_diagnosis_min = self.cleaned_data.get('mentor_age_of_diagnosis_min')
        mentor_age_of_diagnosis_max = self.cleaned_data.get('mentor_age_of_diagnosis_max')
        mentor_condition =self.cleaned_data.get('mentor_condition')
        transplant=self.cleaned_data.get('transplant')
        mentors = User.objects.filter(mentor__isnull=False)
        if mentor_age_of_diagnosis_min is not None:
            mentors = mentors.filter(mentor__age_of_diagnosis__gte=mentor_age_of_diagnosis_min)
        if mentor_age_of_diagnosis_max is not None:
            mentors = mentors.filter(mentor__age_of_diagnosis__lte=mentor_age_of_diagnosis_max)
        if mentor_condition and "any" != mentor_condition :
            mentors = mentors.filter(mentor__condition__icontains=mentor_condition)
        if transplant and "any" != transplant:
            mentors = mentors.filter(mentor__transplant__icontains=transplant)
        return mentors
        
    def filter_by_user_type(self,user_type):
        """Generates a list of users based on user type and user type specific fields"""
        combined_queryset = User.objects.none()
        if "PT" in user_type:
            patients=self.filter_by_patient()
            combined_queryset = combined_queryset | patients
        if "PR" in user_type:
            parents=self.filter_by_parent()
            combined_queryset = combined_queryset | parents
        if "MT" in user_type:
            mentors=self.filter_by_mentor()
            combined_queryset = combined_queryset | mentors
        return combined_queryset
    
    def filter_by_age_range(self,users):
        """Filters users based on age"""
        current_date = timezone.now().date()
        min_age = self.cleaned_data.get('min_age')
        if min_age is not None:
            min_birth_date = current_date - timedelta(days=365.25 * min_age)
            users = users.filter(date_of_birth__lte=min_birth_date)
        max_age = self.cleaned_data.get('max_age')
        if max_age is not None:
            max_birth_date = current_date - timedelta(days=365.25 * (max_age + 1))
            users = users.filter(date_of_birth__gte=max_birth_date)
        return users
        
    def filter_users(self, users):
        """Filters users based on critera provided"""
        user_type = self.cleaned_data.get('user_type')
        if user_type:
            combined_queryset = self.filter_by_user_type(user_type)
            users = users.distinct() & combined_queryset.distinct()
        users = self.filter_by_age_range(users)
        genders = self.cleaned_data.get('gender')
        if genders:
            users = users.filter(gender__in=genders)
        language =self.cleaned_data.get('language')
        if language and "any" != language:
            users = users.filter(language=language)
        ethnicity =self.cleaned_data.get('ethnicity')
        if ethnicity and "any" != ethnicity:
            users = users.filter(ethnicity=ethnicity)
        country =self.cleaned_data.get('country')
        if country and "any" != country:
            users = users.filter(location=country)
        hospital =self.cleaned_data.get('hospital')
        if hospital and "any" != hospital:
            users = users.filter(hospital=hospital)
        return users