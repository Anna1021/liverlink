from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from peer_support.models import Notification


class InboxView(LoginRequiredMixin, View):
    """Display the current user's inbox."""

    def get(self, request):
        """Display the current user's inbox."""
        
        notifications = Notification.objects.filter(user=request.user)
        unviewed_notifications = Notification.objects.filter(user=request.user, viewed=False)
        unviewed_notifications.update(viewed=True)
        return render(request, 'inbox.html', {'notifications': notifications})