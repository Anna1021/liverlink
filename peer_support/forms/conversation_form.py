from django import forms
from peer_support.models import Conversation,GroupConversation,User

class ConversationForm(forms.ModelForm):
    """Form enabling users to create a new conversation"""
    class Meta:
        model = Conversation
        fields = ['users']
        users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),widget=forms.CheckboxSelectMultiple())

    def __init__(self, user, **kwargs):
        """Construct new form instance with a user instance."""
        
        super().__init__(**kwargs)
        self.fields['users'].queryset = User.objects.exclude(username=user.username)

    def save(self,current_user,group=False):
        """Create a new conversation or fetch an existing one"""
        super().save(commit=False)
        new_users = self.cleaned_data.get('users')
        new_users |= User.objects.filter(username = current_user.username)
        if not group:
            existing = set(Conversation.objects.all())
            for user in new_users:
                filtered = User.objects.filter(username=user.username)
                existing = existing.intersection(set(Conversation.objects.filter(users__in=filtered)))
            print(existing)
            if len(existing) > 0:
                conversation = list(existing)[0]
            else:
                conversation = Conversation.objects.create()
                for user in new_users:
                    conversation.add_user(user)
                    user.conversations.add(conversation)
        else:
            conversation = GroupConversation.objects.create()
            for user in new_users:
                conversation.add_user(user)
                user.conversations.add(conversation)
        return conversation