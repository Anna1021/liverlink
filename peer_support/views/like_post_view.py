from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from peer_support.models import Post, Notification


class LikePostView(LoginRequiredMixin, View):
    """Like a post."""

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        liked = True
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            self.send_notification(request, post)
        like_count = post.like_count()
        return JsonResponse({"liked": liked, "like_count": like_count})

    def send_notification(self, request, post):
        """Send a notification to the post author when their post is liked, unless a notification already exists."""

        content_type = ContentType.objects.get_for_model(Post)
        data = {"user": post.author, "notifying_user": request.user, "content_type": content_type, 
                "object_id": post.id, "title": "New Post Like"}
        if not Notification.objects.filter(**data).exists() and post.author != request.user:
            Notification.objects.create(**data)