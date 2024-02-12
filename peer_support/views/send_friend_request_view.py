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
        user=receiver
    )
    return JsonResponse({'status': 'success'})

def accept_friend_request(request):
    friend_request = FriendRequest.objects.get(id=request.POST['friend_request_id'])
    friend_request.status = 'accepted'
    friend_request.save()
    # Update the user's friends list
    friend_request.from_user.friends.add(friend_request.to_user)
    friend_request.to_user.friends.add(friend_request.from_user)