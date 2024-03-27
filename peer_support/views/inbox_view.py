from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from peer_support.models import Notification
from datetime import timedelta
from django.utils import timezone

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
            notifications = self.filter_by_type(notifications, type)
        if timeframe:
            notifications = self.filter_by_timeframe(notifications, timeframe)
        return notifications

    def filter_by_timeframe(self, notifications, timeframe):
        """Filter notifications by the specified timeframe."""

        now = timezone.now()
        if timeframe == 'past_24_hours':
            start_time = now - timedelta(hours=24)
            notifications = notifications.filter(created__gte=start_time, created__lt=now)
        elif timeframe == 'past_7_days':
            start_time = now - timedelta(days=7)
            notifications = notifications.filter(created__gte=start_time, created__lt=now)
        elif timeframe == 'past_4_weeks':
            start_time = now - timedelta(weeks=4)
            notifications = notifications.filter(created__gte=start_time, created__lt=now)
        elif timeframe == 'earlier':
            start_time = now - timedelta(weeks=4)  
            notifications = notifications.filter(created__lt=start_time)
        else:
            notifications = notifications.none()
        return notifications

    def filter_by_type(self, notifications, type):
        """Filter notifications by the specified type."""
        
        if type == 'other':
            return notifications.filter(content_type__isnull=True)
        else:
            return notifications.filter(content_type__model=type.lower().replace(" ", ""))