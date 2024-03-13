from django import forms
from peer_support.models import Feedback

class FeedbackForm(forms.ModelForm):
    """Form enabling users to send feedback."""

    class Meta:
        """Form options."""

        model = Feedback
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3})
        }