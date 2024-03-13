from django.views.generic.edit import FormView
from django.shortcuts import redirect, render,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import Post
from peer_support.forms import PostForm
from .helpers import retrieve_friend_posts

class FeedView(LoginRequiredMixin, FormView):
    """Feed view."""
    
    def get(self,request):
        feed_type = request.GET.get('feed_type','global')  
        user_posts = self.retrieve_posts(request)
        form = PostForm(request.user)
        current_user = request.user 
        if current_user.first_login == True:
            current_user.first_login = False
            current_user.save()
            return render(request, 'feed.html', {'posts': user_posts, 'feed_type': feed_type, 'form':form,'first':True})
        return render(request, 'feed.html', {'posts': user_posts, 'feed_type': feed_type, 'form':form})

    def post(self,request):
        """Submit post"""

        feed_type = request.GET.get('feed_type')  
        user_posts = self.retrieve_posts(request)
        form = PostForm(request.user,data=request.POST)
        if form.is_valid():
            post = form.save()
            return redirect(reverse('feed'), post_id=post.id)
        else:
            return render(request, 'feed.html', {'posts': user_posts, 'feed_type': feed_type, 'form':form})

    # def retrieve_friend_posts(self,request):
    #     user_friends = request.user.friends.all()
    #     # Retrieve the user's posts and friends' posts
    #     return Post.objects.filter(Q(author__in=user_friends) | Q(author=request.user)).order_by("-created_at")

    def retrieve_posts(self,request):
        """Retrieve posts and display them in chronological order."""

        feed_type = request.GET.get('feed_type') 
        user_posts = retrieve_friend_posts(request)
        if feed_type == 'global':
            user_posts = user_posts|Post.objects.filter(visibility='G')
        user_posts = user_posts.order_by("-created_at")
        # else:
        #     user_friends = request.user.friends.all()
        #     # Retrieve the user's posts and friends' posts
        #     user_posts = Post.objects.filter(Q(author__in=user_friends) | Q(author=request.user)).order_by("-created_at")
        return user_posts
        