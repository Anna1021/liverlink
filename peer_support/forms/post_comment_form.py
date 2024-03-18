from django import forms
from peer_support.models import PostComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['content']

    def __init__(self,user,post,**kwargs):
        super().__init__(**kwargs)
        self.author = user
        self.post = post

    def get_parent(self,parent_id):
        if parent_id:
            return PostComment.objects.get(id=parent_id)
        return None

    def save(self,parent_id=None):
        super().save(commit=False)
        comment = PostComment.objects.create(
            author=self.author,
            post=self.post,
            parent=self.get_parent(parent_id),
            content=self.cleaned_data['content']

        )
        return comment
        