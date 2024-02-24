from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render, get_object_or_404 #new404
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from peer_support.forms import LogInForm, PasswordForm, UserForm, SignUpForm
#from peer_support.views.helpers import login_prohibited
#post
from peer_support.models import Post, PostComment
from peer_support.forms import PostForm, CommentForm



def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})




def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        comment_form = CommentForm()
    
    return render(request, 'post_detail.html', {'post': post, 'comment_form': comment_form})


def show_posts(request):
    """Retrive all posts created by the current user"""

    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'show_posts.html', {'user_posts': user_posts})

