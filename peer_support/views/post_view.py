from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import FormView
from peer_support.models import Post, PostComment
from peer_support.forms import CommentForm



class PostView(LoginRequiredMixin,FormView):

    def get(self,request,post_id):
        post = get_object_or_404(Post, pk=post_id)
        comments = PostComment.objects.filter(post=post, parent=None) 
        comment_form = CommentForm()
        return render(request, 'post_detail.html', {'post': post,'comments': comments, 'comment_form': comment_form})

    def post(self,request, post_id):
        """Show the detail of a post and comment on the post"""
        post = get_object_or_404(Post, pk=post_id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_id = request.POST.get('parent_id')
            parent_comment = None
            if parent_id:
                parent_comment = PostComment.objects.get(id=parent_id)
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.parent = parent_comment
            comment.save()
            return redirect('post_detail', post_id=post_id)
        else:
            return render(request, 'post_detail.html', {'form': comment_form})
    
