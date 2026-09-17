from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, reverse, redirect
from django.views import View
from peer_support.models import Report
from .helpers import get_page


class ModerationView(LoginRequiredMixin, View):
    """Display the moderation view."""

    def get(self, request):
        """Display all reports."""

        current_user = request.user
        if not current_user.is_staff:
            messages.error(request, "You do not have access to this view.")
            return redirect(reverse("feed"))
        reports = Report.objects.order_by("-id")
        reports = get_page(request, reports)
        return render(request, "moderation.html", {"reports": reports})
