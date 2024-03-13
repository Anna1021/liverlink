from django import forms
from peer_support.models import Feedback

class FeedbackForm(forms.ModelForm):
    """Form enabling users to send feedback."""

    class Meta:
        """Form options."""

        model = Feedback
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'style': 'width: 700px'}),
            'content': forms.Textarea(attrs={'rows': 5, 'style': 'width: 700px'})
        }