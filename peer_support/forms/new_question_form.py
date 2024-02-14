
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import MaxLengthValidator
from peer_support.models import Question

class NewQuestionForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': 'Query Title'
        }),
        max_length=150,
        validators=[
            MaxLengthValidator(150, message="Title cannot be more than 150 characters long")
        ]
    )
    class Meta:
        model = Question
        fields = ['title', 'body']
