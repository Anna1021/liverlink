from django import forms
from peer_support.models import Post
from .form_choices import POST_VISIBILITY_CHOICES


class PostForm(forms.ModelForm):
    """Form for creating a new post."""

    visibility = forms.ChoiceField(choices=[POST_VISIBILITY_CHOICES])
    class Meta:
        model = Post
        fields = ["visibility", "content"]
        widgets = {"content": forms.Textarea(attrs={"rows": 2, "cols": 50})}

    
    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.author = user

    def save(self):
        super().save(commit=False)
        post = Post.objects.create(
            author=self.author,
            content=self.cleaned_data["content"],
            visibility=self.cleaned_data["visibility"],
        )
        return post
