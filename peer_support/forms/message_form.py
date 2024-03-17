from django import forms
from peer_support.models import Message

class MessageForm(forms.ModelForm):
    """Form enabling users to send messages in a conversation"""

    class Meta:
        model = Message
        fields = ['content']

    def __init__(self,conversation, user=None, **kwargs):
        """Construct new form instance with a conversation and user instance."""
        
        super().__init__(**kwargs)
        self.conversation = conversation
        self.user = user
    
    def get_previous_message(self):
        """Retrieve the last message in the conversation if it exists."""

        if self.conversation.messages.exists():
            return self.conversation.messages.last()
        return None

    def create_message_content(self, previous_message):
        """Create the message content, linking it to the previous message if available."""

        return Message.objects.create(
            sender = self.user,
            content = self.cleaned_data.get('content'),
            previous_message = previous_message,
        )

    def update_message_visibility_and_conversation(self, message):
        """Make the message visible to all conversation users and update their conversations."""

        for user in self.conversation.users.all():
            message.visible_to.add(user)
            user.conversations.add(self.conversation)

    def create_message(self):
        """Create a message in a conversation, maintaining visibility and conversation updates."""

        previous_message = self.get_previous_message()
        message = self.create_message_content(previous_message)
        self.update_message_visibility_and_conversation(message)
        return message

    def save(self):
        """Send message"""

        super().save(commit=False)
        message = self.create_message()
        self.conversation.send(message)
        return message