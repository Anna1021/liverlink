from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, reverse
from peer_support.models import Report, Message, User
from django.contrib import messages

@login_required
def decline_report(request, report_id):
    """Delete report make object viewable"""
    if not request.user.is_staff:
            messages.error(request,"You do not have access to this view.")
            return redirect(reverse('feed'))
    report = get_object_or_404(Report, id=report_id)
    reported_object = report.content_object
    if reported_object:
        if (isinstance(reported_object, Message)):
            reported_object.visible_to.add(report.reporter)  
            reported_object.save()             
        report.delete()
        messages.success(request, "Report and the reported object have been successfully deleted.")
    else:
        messages.error(request, "The reported object could not be found.")
    return redirect('moderation')