from django import forms
from peer_support.forms import UserForm
from peer_support.models import Parent
from .form_choices import CONDITION_CHOICES, TRANSPLANT_CHOICES

class ParentForm(forms.ModelForm):
    """Form to update parent profiles."""

    child_condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=False)
    child_age_of_diagnosis = forms.IntegerField(required=False, min_value=0)
    transplant = forms.ChoiceField(choices=TRANSPLANT_CHOICES, required=False)

    class Meta:
        """Form options."""

        model = Parent
        fields = UserForm.Meta.fields + ['child_condition', 'child_age_of_diagnosis']
        widgets = UserForm.Meta.widgets