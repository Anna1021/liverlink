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

    def save(self):
        """Send message"""
        super().save(commit=False)
        message = Message.objects.create(
            sender=self.user,
            content=self.cleaned_data.get('content'),
        )
        for user in self.conversation.users.all():
            message.visible_to.add(user)
        self.conversation.send(message)
        return message
