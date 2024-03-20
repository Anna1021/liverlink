from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from peer_support.models import User, FriendRequest, Notification

class SendFriendRequestView(LoginRequiredMixin, View):
    """Send a friend request and create a notification."""

    def get(self, request, user_id):
        """Send a friend request."""

        receiver = User.objects.get(id=user_id)
        FriendRequest.objects.create(sender=request.user, receiver=receiver)
        Notification.objects.create(user=receiver, notifying_user=request.user, content_object=FriendRequest.objects.last())
        return JsonResponse({'status': 'success'})