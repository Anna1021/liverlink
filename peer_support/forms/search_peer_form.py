from django import forms
from django.db.models import Q

class SearchPeerForm(forms.Form):
    """Form enabling the searching of users"""

    search = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

    def search_users(self, users):
        """Searches for term in username"""
        
        search_term = self.cleaned_data.get('search', '').strip()
        if search_term:
            users = users.filter(Q(username__icontains=search_term) | Q(first_name__icontains=search_term)|Q(last_name__icontains=search_term))
        return users