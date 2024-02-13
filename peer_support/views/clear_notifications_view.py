from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from peer_support.models import Notification

@login_required
def clear_notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    notifications.delete()

    return redirect('inbox')