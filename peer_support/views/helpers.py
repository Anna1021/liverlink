from django.conf import settings
from django.shortcuts import redirect
from peer_support.models import Notification

def login_prohibited(view_function):
    """Decorator for view functions that redirect users away if they are logged in."""
    
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function

def notifications(request):
    if request.user.is_authenticated:
        has_unviewed_notifications = Notification.objects.filter(user=request.user, viewed=False).exists()
        return {'has_unviewed_notifications': has_unviewed_notifications}
    else:
        return {'has_unviewed_notifications': False}