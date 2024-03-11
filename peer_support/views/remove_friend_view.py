from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from peer_support.models import User

@login_required
def remove_friend(request, user_id):
    """Remove a friend from current user's friends list."""
    friend = User.objects.get(id=user_id)
    request.user.friends.remove(friend)
    return JsonResponse({'status': 'success'})