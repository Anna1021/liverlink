from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import Feedback


class FeedbackView(LoginRequiredMixin, View):
    """Displays all user feedback."""

    template_name = "feedback.html"

    def get(self, request):
        """Display all user feedback."""

        current_user = request.user
        if not current_user.is_staff:
            messages.error(request, "You do not have access to this view.")
            return redirect(reverse("feed"))
        feedback = Feedback.objects.order_by("-submitted_at")
        return render(request, "feedback.html", {"feedback": feedback})
