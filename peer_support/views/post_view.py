from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import FormView
from peer_support.models import Post, PostComment, Notification
from peer_support.forms import CommentForm, ReportForm
from .helpers import get_post
from django.contrib import messages


class PostView(LoginRequiredMixin, FormView):
    """Show the detail of a post and comment on the post"""

    def get(self, request, post_id):
        post = get_post(request, post_id)
        if not post:
            messages.error(request, "This post does not exist")
            return redirect("feed")
        if post.author in request.user.blocked_users.all() or request.user in post.author.blocked_users.all():
            messages.error(request, "You cannot view this post!")
            return redirect('feed')
        post.liked_by_user = post.likes.filter(id=request.user.id).exists()
        comments = PostComment.objects.filter(post=post, parent=None) 
        comment_form = CommentForm(request.user,post)
        return render(request, 'post_detail.html', {'post': post,'comments': comments, 'comment_form': comment_form,'report_form': ReportForm()})

    def post(self, request, post_id):
        if 'report_comment' in request.POST:
            comment_id = request.POST.get('action')
            self.comment_report(request, comment_id)
        elif 'report_post' in request.POST:
            post_id = request.POST.get('action')
            self.post_report(request, post_id)
        else:
            self.comment_submission(request, post_id)
        return redirect('post_detail', post_id=post_id)
    
    def comment_report(self, request, comment_id):
        comment = get_object_or_404(PostComment, id=comment_id)
        report_form = ReportForm(request.POST)
        if report_form.is_valid():
            report_form.save_report_for_object(comment, request.user)
            messages.success(request, "Comment reported successfully.")
        else:
            messages.error(request, "There was an issue with the report.")

    def post_report(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        report_form = ReportForm(request.POST)
        if report_form.is_valid():
            report_form.save_report_for_object(post, request.user)
            messages.success(request, "Post reported successfully.")
        else:
            messages.error(request, "There was an issue with the post.")

    def comment_submission(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        form = CommentForm(request.user, post, data=request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent_id')
            comment = form.save(parent_id)
            self.send_notification(comment)
            return redirect('post_detail', post_id=post_id)
        else:
            messages.error(request, "There was an issue with the report.")

    def send_notification(self, comment):
        if comment.post.author != comment.author:
            Notification.objects.create(content_object=comment, user=comment.post.author, notifying_user=comment.author)
        if comment.parent and comment.parent.author != comment.author:
            Notification.objects.create(content_object=comment, user=comment.parent.author, notifying_user=comment.author,
                                        description=f"{comment.author} has replied to your comment.")