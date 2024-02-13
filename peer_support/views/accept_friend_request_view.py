from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from peer_support.models import Notification, FriendRequest

@login_required
def accept_friend_request(request, friend_request_id, notification_id):
    friend_request = FriendRequest.objects.get(id=friend_request_id)
    friend_request.is_accepted = True
    friend_request.save()
    Notification.objects.create(
        title='Friend Request Accepted',
        description=f'{request.user.username} accepted your friend request.',
        user=friend_request.sender
    )
    user = request.user
    user.friends.add(friend_request.sender)

    messages.add_message(request, messages.SUCCESS, f"You are now friends with {friend_request.sender}!")

    return redirect('delete_notification', notification_id=notification_id)