from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from peer_support.models import Notification
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

@csrf_exempt
def delete_notification(request, notification_id):
    print('delete_notification')
    notification = get_object_or_404(Notification, id=notification_id)
    if notification.friend_request:
        notification.friend_request.delete()
    notification.delete()
    return redirect('inbox')