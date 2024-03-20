from django.views import View
from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .helpers import get_post, get_comment

class DeleteCommentView(LoginRequiredMixin, View):
    """Delete comment"""
    
    def get(self, request, comment_id):
        """Checks user is authorised to delete comment then deletes it"""

        comment = get_comment(comment_id)
        post = None
        if comment:
            post = get_post(request, comment.post.id)
        if not post or not comment:
            messages.error(request, "This comment does not exist.")
            return redirect('feed')
        if comment.author != request.user:
            messages.add_message(request, messages.ERROR, "This comment does not exist")
            return redirect('feed')
        comment.delete()
        messages.success(request, "Comment successfully deleted.")
        return redirect(reverse('post_detail', kwargs={'post_id':post.id}))