from django.views import View
from peer_support.models import Post
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class DeletePostView(LoginRequiredMixin,View):
    def get(self,request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.author == request.user:
            post.delete()
        else:
            print("User is not authorized to delete this post.")
        return redirect('feed')
