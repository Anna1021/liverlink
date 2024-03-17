from django import forms
from peer_support.models import GroupConversation, User

class AddUsersForm(forms.ModelForm):
    """Form enabling users to add users to an existing conversation"""

    class Meta:
        model = GroupConversation
        fields = ['users']
        users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True)

    def __init__(self, user, conversation, **kwargs):
        """Construct new form instance with a user and conversation instance."""
        
        super().__init__(**kwargs)
        self.fields['users'].queryset = user.friends.exclude(id__in=conversation.users.all())

    def save(self, conversation):
        """Add users to the conversation"""

        super().save(commit=False)
        new_users = self.cleaned_data.get('users')
        conversation.add_users(new_users)
        return conversation