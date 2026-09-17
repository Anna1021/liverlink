from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from peer_support.models import Notification
from peer_support.views.helpers import filter_notifications

@login_required
def clear_notifications(request):
    """Clear visible notifications for the current user."""

    notifications = Notification.objects.filter(user=request.user)
    notifications = filter_notifications(request, notifications)
    notifications.delete()
    return redirect("inbox")