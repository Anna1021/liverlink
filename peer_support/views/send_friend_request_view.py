from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from peer_support.models import Notification, User, FriendRequest


class SendFriendRequestView(LoginRequiredMixin, View):
    """Send a friend request and create a notification."""

    def get(self, request, user_id):
        """Send a friend request."""

        receiver = User.objects.get(id=user_id)
        FriendRequest.objects.create(sender=request.user, receiver=receiver)
        self.send_notification(request, receiver)
        return JsonResponse({"status": "success"})

    def send_notification(self, request, receiver):
        """Send a notification."""

        Notification.objects.create(
            title="Friend Request",
            description=f"{request.user.username} sent you a friend request.",
            user=receiver,
            friend_request=FriendRequest.objects.last(),
        )
