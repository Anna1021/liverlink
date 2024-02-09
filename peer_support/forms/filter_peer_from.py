from django import forms
from peer_support.models import User
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

    age_of_diagnosis_min = forms.IntegerField(required=False)
    age_of_diagnosis_max = forms.IntegerField(required=False)
    condition=forms.CharField(max_length=255, required=False)

    child_age_of_diagnosis_min = forms.IntegerField(required=False)
    child_age_of_diagnosis_max = forms.IntegerField(required=False)
    child_condition=forms.CharField(max_length=255, required=False)
    

    def __init__(self, *args, **kwargs):
        """Initialise query set with users tasks"""

        super(FilterPeerForm, self).__init__(*args, **kwargs)
        
    def filter_users(self, users):
        """Filters users based on critera provided"""
        age_of_diagnosis_min = self.cleaned_data.get('age_of_diagnosis_min')
        age_of_diagnosis_max = self.cleaned_data.get('age_of_diagnosis_max')
        condition =self.cleaned_data.get('condition')

        child_age_of_diagnosis_min = self.cleaned_data.get('child_age_of_diagnosis_min')
        child_age_of_diagnosis_max = self.cleaned_data.get('child_age_of_diagnosis_max')
        child_condition =self.cleaned_data.get('child_condition')

        user_type = self.cleaned_data.get('user_type')
        if user_type:
            combined_queryset = User.objects.none()

            if "patient" in user_type:
                patients = User.objects.filter(patient__isnull=False)
                if age_of_diagnosis_min is not None:
                    patients = patients.filter(patient__age_of_diagnosis__gte=age_of_diagnosis_min)
                if age_of_diagnosis_max is not None:
                    patients = patients.filter(patient__age_of_diagnosis__lte=age_of_diagnosis_max)
                if condition:
                    patients = patients.filter(patient__condition__icontains=condition)
                combined_queryset = combined_queryset | patients

            if "parent" in user_type:
                parents = User.objects.filter(parent__isnull=False)
                if child_age_of_diagnosis_min is not None:
                    parents = parents.filter(parent__child_age_of_diagnosis__gte=child_age_of_diagnosis_min)
                if child_age_of_diagnosis_max is not None:
                    parents = parents.filter(parent__child_age_of_diagnosis__lte=child_age_of_diagnosis_max)
                if child_condition:
                    parents = parents.filter(parent__child_condition__icontains=child_condition)
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