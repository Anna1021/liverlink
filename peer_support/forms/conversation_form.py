from django import forms
from peer_support.models import Conversation, GroupConversation, User


class ConversationForm(forms.ModelForm):
    """Form enabling users to create a new conversation"""

    class Meta:
        model = Conversation
        fields = ["users"]
        users = forms.ModelMultipleChoiceField(
            queryset=User.objects.all(),
            widget=forms.CheckboxSelectMultiple(),
            required=True,
        )

    def __init__(self, user, **kwargs):
        """Construct new form instance with a user instance."""

        super().__init__(**kwargs)
        self.fields["users"].queryset = user.friends.all()

    def filter_existing_conversations_by_users(self, new_users):
        """Filter existing conversations to those containing the new users."""

        existing_conversations = set(Conversation.objects.all())
        for user in new_users:
            user_conversations = set(Conversation.objects.filter(users__in=[user]))
            existing_conversations = existing_conversations.intersection(user_conversations)
        return existing_conversations

    def remove_group_conversations(self, conversations):
        """Remove group conversations from the existing set, retaining only direct conversations."""

        return {convo for convo in conversations if convo.as_group() is None}

    def get_direct_conversation(self, new_users):
        """Return existing direct conversation if it exists or create a new one."""

        existing_conversations = self.filter_existing_conversations_by_users(new_users)
        direct_conversations = self.remove_group_conversations(existing_conversations)
        if direct_conversations:
            return list(direct_conversations)[0]
        conversation = Conversation.objects.create()
        conversation.add_users(new_users)
        return conversation

    def save(self, current_user, group=False):
        """Create a new conversation or fetch an existing one."""

        super().save(commit=False)
        new_users = self.cleaned_data.get("users")
        new_users |= User.objects.filter(username=current_user.username)
        if not group:
            conversation = self.get_direct_conversation(new_users)
            current_user.conversations.add(conversation)
        else:
            conversation = GroupConversation.objects.create()
            conversation.add_users(new_users)
        return conversation
