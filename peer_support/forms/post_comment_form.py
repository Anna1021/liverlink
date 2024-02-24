from django import forms
from peer_support.models import PostComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['content']
