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

    def get_existing_conversations(self,ctr,existing):
        """Return list of existing conversations containing specified users"""
        convo = list(existing)[ctr]
        if convo.as_group() is not None:
            existing.remove(convo)
        else:
            ctr+=1
        return ctr, existing


    def get_direct_conversation(self,new_users):
        """Return existing direct conversation if it exists or create a new one"""
        existing = set(Conversation.objects.all())
        for user in new_users:
            filtered = User.objects.filter(username=user.username)
            existing = existing.intersection(set(Conversation.objects.filter(users__in=filtered)))
        ctr = 0
        while ctr < len(existing):
            ctr, existing = self.get_existing_conversations(ctr,existing)
        if len(existing) > 0:
            conversation = list(existing)[0]
        else:
            conversation = Conversation.objects.create()
            conversation.add_users(new_users)
        return conversation

    def save(self,current_user,group=False):
        """Create a new conversation or fetch an existing one"""
        super().save(commit=False)
        new_users = self.cleaned_data.get('users')
        new_users |= User.objects.filter(username = current_user.username)
        if not group:
            conversation = self.get_direct_conversation(new_users)
        else:
            conversation = GroupConversation.objects.create()
            conversation.add_users(new_users)
        return conversation