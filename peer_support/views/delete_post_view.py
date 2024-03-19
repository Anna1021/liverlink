from django.views import View
from peer_support.models import Post
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .helpers import get_post

class DeletePostView(LoginRequiredMixin,View):
    """Delete post"""
    
    def get(self,request, post_id):
        post = get_post(request,post_id)
        if not post:
            messages.error(request,"This post does not exist.")
            return redirect('feed')
        if post.author != request.user:
            messages.error(request, "You are not authorised to delete this post.")
            return redirect('feed')
        post.delete()
        return redirect('feed')
    