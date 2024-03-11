from django.views import View
from peer_support.models import Post
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class DeletePostView(LoginRequiredMixin,View):
    """Delete post"""
    
    def get(self,request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.author == request.user:
            post.delete()
        else:
            messages.error(request, "You are not authorized to delete this post.")
        return redirect('feed')
    