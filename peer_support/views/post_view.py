from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import FormView
from peer_support.models import Post, PostComment
from peer_support.forms import CommentForm
from .helpers import get_post


class PostView(LoginRequiredMixin,FormView):

    def get(self, request, post_id):
        post = get_post(request,post_id)
        if not post:
            return redirect('feed')
        comments = PostComment.objects.filter(post=post, parent=None) 
        comment_form = CommentForm(request.user, post)
        liked_by_current_user = self.liked_by_current_user(post, request.user)
        return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

    def post(self, request, post_id):
        """Show the detail of a post and comment on the post"""
        post = get_object_or_404(Post, pk=post_id)
        comments = PostComment.objects.filter(post=post, parent=None)
        form = CommentForm(request.user,post,data=request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent_id')
            form.save(parent_id)
            return redirect('post_detail', post_id=post_id)
        else:
            return render(request, 'post_detail.html', {'post': post,'comments': comments,'comment_form': form})
    
