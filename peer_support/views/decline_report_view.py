from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from peer_support.models import Report

@login_required
def decline_report(request, report_id):
    """Delete report make object viewable"""
    report = get_object_or_404(Report, id=report_id)
    reported_object = report.content_object
    # Check if the reported object has an attribute 'is_reported'
    if hasattr(reported_object, 'is_reported'):
        reported_object.is_reported = False
        reported_object.save()
    report.delete()
    return redirect('moderation')