from django import forms
from peer_support.models import User
from .helpers import validate_min_age


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "date_of_birth",
            "gender",
            "location",
            "hospital",
            "ethnicity",
            "language",
            "bio",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get("date_of_birth")
        validate_min_age(dob)
        return dob
