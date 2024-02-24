""" from django.conf import settings
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



def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = None #initialise comment 
    print("Request Method:", request.method) #debug 

    if request.method == 'POST':
        print("Inside POST block") #debug
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            print("Comment saved successfully:", comment) #debug
            # Redirect to the post_detail after adding the comment
            return redirect(reverse('post_detail', kwargs={'post_id': post_id}))
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'form': form, 'new_comment': comment}) 
 """