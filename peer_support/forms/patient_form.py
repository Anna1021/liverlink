from django import forms
from peer_support.forms import UserForm
from peer_support.models import Parent

class ParentForm(forms.ModelForm):
    """Form to update parent profiles."""

    class Meta:
        """Form options."""

        model = Parent
        fields = UserForm.Meta.fields + ['child_condition', 'child_age_of_diagnosis']
        widgets = UserForm.Meta.widgets