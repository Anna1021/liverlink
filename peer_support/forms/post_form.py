from django import forms
from peer_support.models import Post

class PostForm(forms.ModelForm):
    """Form to ask user for post content.
    The post author must be by the post creator.
    """
    class Meta:

        model = Post
        fields = ['visibility', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows':2,'cols':50})

        }
    visibility = forms.ChoiceField(choices=[
                ("G","Global"),
                ("F","Friends")
            ])

    def __init__(self,user,**kwargs):
        super().__init__(**kwargs)
        self.author = user

    def save(self):
        super().save(commit=False)
        post = Post.objects.create(
            author=self.author,
            content=self.cleaned_data['content'],
            visibility=self.cleaned_data['visibility']
        )
        return post
