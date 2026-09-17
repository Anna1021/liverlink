from django.shortcuts import get_object_or_404, redirect, reverse
from peer_support.models import Report, Message
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class DeclineReportView(LoginRequiredMixin, View):
    """Deletes report and restores related object."""

    def get(self, request, report_id):
        if not request.user.is_staff:
            messages.error(request, "You do not have access to this view.")
            return redirect(reverse("feed"))
        report = get_object_or_404(Report, id=report_id)
        success = self.process_reported_object(report)
        if success:
            messages.success(request, "Report has been successfully deleted.")
        else:
            messages.error(request, "The reported object could not be found.")
        return redirect("moderation")

    def process_reported_object(self, report):
        """Processes the reported object based on its type."""

        reported_object = report.content_object
        report.delete()
        if not reported_object:
            return False
        if isinstance(reported_object, Message):
            self.handle_reported_message(report, reported_object)
        return True

    def handle_reported_message(self, report, reported_object):
        reported_object.visible_to.add(report.reporter)
        reported_object.save()
