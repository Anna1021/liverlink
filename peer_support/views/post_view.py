from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from peer_support.forms import LogInForm, PasswordForm, UserForm, SignUpForm
from peer_support.views.helpers import login_prohibited
#post
from peer_support.models import Post, PostComment
from peer_support.forms import PostForm, CommentForm
from django.db.models import Q


#@login_required
def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed') 
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


def post_detail(request, post_id):
    """Show the detail of a post and comment on the post"""
    post = get_object_or_404(Post, pk=post_id)
    comments = PostComment.objects.filter(post=post, parent=None) # filter out parent comment
        

    if request.method == 'POST':
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
        comment_form = CommentForm()
    return render(request, 'post_detail.html', {'post': post,'comments': comments, 'comment_form': comment_form})
    #return render(request, 'post_detail.html', {'post': post, 'comment_form': comment_form})

def feed(request):
    feed_type = request.GET.get('feed_type', 'global')  
    user_posts = None

    if feed_type == 'global':
        user_posts = Post.objects.all().order_by("-created_at")
    elif feed_type == 'friends':
        user_friends = request.user.friends.all()
        # Retrieve both the user's own posts and posts from user's friends
        user_posts = Post.objects.filter(Q(author__in=user_friends) | Q(author=request.user)).order_by("-created_at")
    return render(request, 'feed.html', {'posts': user_posts, 'feed_type': feed_type})
    