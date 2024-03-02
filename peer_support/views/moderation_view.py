from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from peer_support.models import Report

class ModerationView(LoginRequiredMixin, View):
    """Display the moderation view."""

    def get(self, request):
        """Display all reports."""
        reports=Report.objects.all()
        return render(request,'moderation.html',{'reports':reports})