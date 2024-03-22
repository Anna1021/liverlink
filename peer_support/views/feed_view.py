from django.views.generic.edit import FormView
from django.shortcuts import redirect, render,reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import Post
from peer_support.forms import PostForm, ReportForm
from .helpers import retrieve_friend_posts
from django.contrib import messages

class FeedView(LoginRequiredMixin, FormView):
    """Displays posts on both global and friend feeds."""
    
    def get(self,request):
        feed_type = request.GET.get('feed_type','global')  
        user_posts = self.retrieve_posts(request)
        form = PostForm(request.user)
        current_user = request.user 
        if current_user.first_login == True:
            current_user.first_login = False
            current_user.save()
            return render(request, 'feed.html', {'posts': user_posts, 'feed_type': feed_type, 'form':form, 'report_form': ReportForm(),'first':True})
        return render(request, 'feed.html', {'posts': user_posts, 'feed_type': feed_type, 'form':form, 'report_form': ReportForm()})

    def post(self,request):
        if 'report_post' in request.POST:
            post_id = request.POST.get('action')
            self.comment_post(request, post_id)
            return redirect(reverse('feed'))
        form = PostForm(request.user,data=request.POST)
        if form.is_valid():
            post = form.save()
            return redirect(reverse('feed'), post_id=post.id)
        else:
            feed_type = request.GET.get('feed_type')
            user_posts = self.retrieve_posts(request)
            return render(request, 'feed.html', {'posts': user_posts, 'feed_type': feed_type, 'form':form})

    def retrieve_posts(self,request):
        """Retrieve posts and display them in chronological order."""

        feed_type = request.GET.get('feed_type') 
        user_posts = retrieve_friend_posts(request)
        if feed_type != 'friends':
            user_posts = user_posts|Post.objects.filter(visibility='G')
        user_posts = user_posts.order_by("-created_at")
        return user_posts

    def comment_post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        report_form = ReportForm(request.POST)
        if report_form.is_valid():
            report_form.save_report_for_object(post, request.user)
            messages.success(request, "Post reported successfully.")
        else:
            messages.error(request, "There was an issue with the report.")