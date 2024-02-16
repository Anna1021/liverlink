from django import forms
from peer_support.models import Post, PostComment

class PostForm(forms.ModelForm):
    """Form to ask user for post text.
    The post author must be by the post creator.
    """
    class Meta:

        model = Post
        fields = ['text']
        widgets = {
            'text': forms.Textarea()
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['content']
