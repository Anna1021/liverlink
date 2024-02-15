from django import forms
from peer_support.models import Conversation,GroupConversation,User

class ConversationForm(forms.ModelForm):
    """Form enabling users to create a new conversation"""
    class Meta:
        model = Conversation
        fields = ['users']
        users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),widget=forms.CheckboxSelectMultiple(),required=True)

    def __init__(self, user, **kwargs):
        """Construct new form instance with a user instance."""
        
        super().__init__(**kwargs)
        self.fields['users'].queryset = user.friends.all()

    def save(self,current_user,group=False):
        """Create a new conversation or fetch an existing one"""
        if not self.is_valid():
            for field, errors in self.errors.items():
                # Iterate through each field and its corresponding error messages
                print(f"Field '{field}': {', '.join(errors)}")
        super().save(commit=False)
        new_users = self.cleaned_data.get('users')
        new_users |= User.objects.filter(username = current_user.username)
        if not group:
            existing = set(Conversation.objects.all())
            for user in new_users:
                filtered = User.objects.filter(username=user.username)
                existing = existing.intersection(set(Conversation.objects.filter(users__in=filtered)))
            ctr = 0
            while ctr < len(existing):
                convo = list(existing)[ctr]
                if convo.as_group() is not None:
                    existing.remove(convo)
                else:
                    ctr+=1
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