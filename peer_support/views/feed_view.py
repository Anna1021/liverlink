
from django.views.generic.edit import FormView
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import Post
from peer_support.forms import PostForm
from django.db.models import Q
class FeedView(LoginRequiredMixin, FormView):
    def get(self,request):
        feed_type = request.GET.get('feed_type', 'global')  
        user_posts = None
        form = PostForm()
        if feed_type == 'global':
            user_posts = Post.objects.all().order_by("-created_at")
        elif feed_type == 'friends':
            user_friends = request.user.friends.all()
            # Retrieve both the user's own posts and posts from user's friends
            user_posts = Post.objects.filter(Q(author__in=user_friends) | Q(author=request.user)).order_by("-created_at")
        return render(request, 'feed.html', {'posts': user_posts, 'feed_type': feed_type, 'form':form})

    def post(self,request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed') 
        