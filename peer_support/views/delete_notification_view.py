from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from peer_support.models import Notification

@login_required
def delete_notification(request, notification_id):
    """Delete a notification."""
    
    notification = get_object_or_404(Notification, id=notification_id)
    if notification.friend_request:
        notification.friend_request.delete()
    notification.delete()
    return redirect('inbox')