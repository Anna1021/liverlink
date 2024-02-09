from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from peer_support.models import User, Parent, Patient

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