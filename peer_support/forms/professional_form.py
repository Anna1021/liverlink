from django import forms
from peer_support.forms import UserForm
from peer_support.models import Professional
from .form_choices import CONDITION_CHOICES

class ProfessionalForm(UserForm, forms.ModelForm):
    """Form to update professional profiles."""

    expertise = forms.ChoiceField(choices=CONDITION_CHOICES, required=False)

    class Meta:
        """Form options."""

        model = Professional
        fields = UserForm.Meta.fields + ['expertise']
        widgets = UserForm.Meta.widgets