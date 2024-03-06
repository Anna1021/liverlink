from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import Post
from django.db.models import Q
class FeedView(LoginRequiredMixin, View):
    def get(self,request):
        feed_type = request.GET.get('feed_type', 'global')  
        user_posts = None

        if feed_type == 'global':
            user_posts = Post.objects.all().order_by("-created_at")
        elif feed_type == 'friends':
            user_friends = request.user.friends.all()
            # Retrieve both the user's own posts and posts from user's friends
            user_posts = Post.objects.filter(Q(author__in=user_friends) | Q(author=request.user)).order_by("-created_at")
        return render(request, 'feed.html', {'posts': user_posts, 'feed_type': feed_type})
        