from django import forms
from peer_support.forms import UserForm
from peer_support.models import Parent
from .form_choices import CONDITION_CHOICES, TRANSPLANT_CHOICES
from .helpers import validate_min_age


class ParentForm(forms.ModelForm):
    """Form to update parent profiles."""

    child_condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    child_age_of_diagnosis = forms.IntegerField(required=False, min_value=0)
    child_transplant = forms.ChoiceField(choices=TRANSPLANT_CHOICES, required=False)

    class Meta:
        """Form options."""

        model = Parent
        fields = UserForm.Meta.fields + [
            "child_condition",
            "child_age_of_diagnosis",
            "child_transplant",
        ]
        widgets = UserForm.Meta.widgets

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get("date_of_birth")
        validate_min_age(dob)
        return dob
