from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from peer_support.models import Notification
from peer_support.views.helpers import filter_by_timeframe, filter_by_type

class InboxView(LoginRequiredMixin, View):
    """Display the current user's inbox."""

    def get(self, request):
        """Display the current user's inbox."""
        
        notifications = Notification.objects.filter(user=request.user)
        notifications = self.filter_notifications(request, notifications)
        unviewed_notifications = Notification.objects.filter(user=request.user, viewed=False)
        unviewed_notifications.update(viewed=True)
        return render(request, 'inbox.html', {'notifications': notifications})
    
    def filter_notifications(self, request, notifications):
        """Filter notifications by type and/or timeframe."""
        
        type = request.GET.get('type', None)
        timeframe = request.GET.get('timeframe', None)
        if type:
            notifications = filter_by_type(notifications, type)
        if timeframe:
            notifications = filter_by_timeframe(notifications, timeframe)
        return notifications