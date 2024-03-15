from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from peer_support.models import Notification, FriendRequest

class AcceptFriendRequestView(LoginRequiredMixin, View):
    """Accept a friend request and create a notification."""

    def get(self, request, friend_request_id, notification_id):
        friend_request = FriendRequest.objects.get(id=friend_request_id)
        friend_request.is_accepted = True
        friend_request.save()
        self.send_notification(request, friend_request)
        request.user.friends.add(friend_request.sender)
        messages.add_message(request, messages.SUCCESS, f"You are now friends with {friend_request.sender}!")
        return redirect('delete_notification', notification_id=notification_id)

    def send_notification(self, request, friend_request):
        """Send a notification."""
        
        Notification.objects.create(
            title='Friend Request Accepted',
            description=f'{request.user.username} accepted your friend request.',
            user=friend_request.sender
        )