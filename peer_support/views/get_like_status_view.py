from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from peer_support.models import Post


@login_required
def get_like_status(request, post_id):
    """Retrieve the initial like status of a post for the current user."""

    post = get_object_or_404(Post, id=post_id)
    liked = request.user in post.likes.all()
    return JsonResponse({"liked": liked})
