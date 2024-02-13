from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from peer_support.models import Notification, User, FriendRequest

@login_required
def send_friend_request(request, user_id):
    receiver = User.objects.get(id=user_id)
    FriendRequest.objects.create(sender=request.user, receiver=receiver)
    Notification.objects.create(
        title='Friend Request',
        description=f'{request.user.username} sent you a friend request.',
        user=receiver,
        friend_request=FriendRequest.objects.last()
    )
    return JsonResponse({'status': 'success'})