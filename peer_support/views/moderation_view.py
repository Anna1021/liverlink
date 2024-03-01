from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from peer_support.models import Report

class ModerationView(LoginRequiredMixin, View):
    """Display the current user's inbox."""

    def get(self, request):
        """Display the current user's inbox."""
        reports=Report.objects.all()
        return render(request,'moderation.html',{'reports':reports})