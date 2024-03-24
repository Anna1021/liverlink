from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from peer_support.models import Post


@login_required
def like_post(request, post_id):
    """Like a post."""

    post = get_object_or_404(Post, id=post_id)
    liked = True
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
    like_count = post.like_count()
    return JsonResponse({"liked": liked, "like_count": like_count})
