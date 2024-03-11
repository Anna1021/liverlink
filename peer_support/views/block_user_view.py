from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from peer_support.models import User, FriendRequest, Notification
from django.db.models import Q

class BlockUserView(LoginRequiredMixin, View):
    """Block the specified user."""

    def get(self, request, user_id):
        """Block the specified user and delete all corresponding relationships and objects."""
        
        blocked_user = User.objects.get(id=user_id)
        request.user.blocked_users.add(blocked_user)
        if blocked_user in request.user.friends.all():
            request.user.friends.remove(blocked_user)
        friend_requests = FriendRequest.objects.filter((Q(sender=blocked_user) & Q(receiver = request.user)) | (Q(sender=request.user) & Q(receiver=blocked_user)))
        friend_request_notifications = Notification.objects.filter(friend_request__in=friend_requests)
        friend_requests.delete()
        friend_request_notifications.delete()
        return JsonResponse({'status': 'success'})