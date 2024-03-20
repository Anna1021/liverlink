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
        self.delete_friend_request(request, blocked_user)
        return JsonResponse({'status': 'success'})
    
    def delete_friend_request(self, request, blocked_user):
        """Delete any existing friend requests and associated notifications between the current user and blocked user."""
        
        friend_requests = FriendRequest.objects.filter((Q(sender=blocked_user) & Q(receiver=request.user)) | (Q(sender=request.user) & Q(receiver=blocked_user)))
        self.delete_friend_request_notifications(request, blocked_user)
        friend_requests.delete()

    def delete_friend_request_notifications(self, request, blocked_user):
        """Delete any existing notifications referencing these friend requests."""

        notifications = Notification.objects.filter((Q(user=blocked_user) & Q(notifying_user=request.user)) | (Q(user=request.user) & Q(notifying_user=blocked_user)))
        notifications.delete()
