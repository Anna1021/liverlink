from django import forms
from peer_support.models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""
        
        super().__init__(**kwargs)
        self.user = user

    def save(self):
        super().save(commit=False)
        message = Message.objects.create(
            sender=self.user,
            content=self.cleaned_data.get('content')
        )
        return message
