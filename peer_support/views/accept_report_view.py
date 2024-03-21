from django.shortcuts import get_object_or_404, redirect, reverse
from peer_support.models import Report, Message, User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class AcceptReportView(LoginRequiredMixin, View):
    """Delete report and remove object attached"""

    def get(self, request, report_id):
        if not request.user.is_staff:
            messages.error(request, "You do not have access to this view.")
            return redirect(reverse("feed"))
        report = get_object_or_404(Report, id=report_id)
        success = self.process_reported_object(report)
        if success:
            messages.success(
                request,
                "Report and the reported object have been successfully deleted.",
            )
        else:
            messages.error(request, "The reported object could not be found.")
        return redirect("moderation")

    def process_reported_object(self, report):
        """Processes the reported object based on its type."""

        reported_object = report.content_object
        if not reported_object:
            return False
        if isinstance(reported_object, Message):
            self.handle_reported_message(reported_object)
        else:
            self.handle_reported_user(reported_object)
        report.delete()
        return True

    def handle_reported_message(self, message):
        all_users = User.objects.all()
        message.delete(all_users)

    def handle_reported_user(self, user):
        user.is_active = False
        user.save()
