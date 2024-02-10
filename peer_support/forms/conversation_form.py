from django import forms
from peer_support.models import Conversation,User

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['users']
        users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),widget=forms.CheckboxSelectMultiple())

    def __init__(self, user, **kwargs):
        """Construct new form instance with a user instance."""
        
        super().__init__(**kwargs)
        self.fields['users'].queryset = User.objects.exclude(username=user.username)

    def save(self,current_user,group=False):
        super().save(commit=False)
        new_users = self.cleaned_data.get('users')
        if not group:
            existing = Conversation.objects.filter(users__in=new_users)
            print(existing)
            if existing.count() > 1:
                conversation = existing[0]
            else:
                new_users |= User.objects.filter(username = current_user.username)
                conversation = Conversation.objects.create()
                for user in new_users:
                    conversation.add_user(user)
                    user.conversations.add(conversation)
        else:
            new_users |= User.objects.filter(username = current_user.username)
            conversation = GroupConversation.objects.create()
            for user in new_users:
                conversation.add_user(user)
                user.conversations.add(conversation)
        return conversation