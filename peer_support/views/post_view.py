from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.views.generic.edit import FormView
from peer_support.models import Post, PostComment
from peer_support.forms import CommentForm, ReportForm
from .helpers import get_post
from django.contrib import messages


class PostView(LoginRequiredMixin,FormView):

    def get(self,request,post_id):
        post = get_post(request,post_id)
        if not post:
            messages.error(request,"This post does not exist")
            return redirect('feed')
        comments = PostComment.objects.filter(post=post, parent=None) 
        comment_form = CommentForm(request.user,post)
        return render(request, 'post_detail.html', {'post': post,'comments': comments, 'comment_form': comment_form,'report_form': ReportForm()})

    def post(self,request, post_id):
        """Show the detail of a post and comment on the post"""
        comment_id = request.POST.get('action')
        if comment_id:
            self.report_submission(request, comment_id)
        else:
            self.comment_submission(request, post_id)
        return redirect('post_detail', post_id=post_id)
    
    def report_submission(self, request, comment_id):
        """Handle report form submission."""
        
        comment = get_object_or_404(PostComment, id=comment_id)
        report_form = ReportForm(request.POST)
        if report_form.is_valid():
            report_form.save_report_for_object(comment, request.user)
            messages.success(request, "Profile reported successfully.")
        else:
            messages.error(request, "There was an issue with the report.")
    
    def comment_submission(self,request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        form = CommentForm(request.user,post,data=request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent_id')
            form.save(parent_id)
    
