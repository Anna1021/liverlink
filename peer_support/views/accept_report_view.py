from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, reverse
from peer_support.models import Report, Message, User
from django.contrib import messages

@login_required
def accept_report(request, report_id):
    """Deletes report and object attached."""
    if not request.user.is_staff:
        messages.error(request,"You do not have access to this view.")
        return redirect(reverse('dashboard'))
    report = get_object_or_404(Report, id=report_id)
    reported_object = report.content_object
    if reported_object:
        all_users = User.objects.all()
        reported_object.delete(all_users)  
        report.delete()
        messages.success(request, "Report and the reported object have been successfully deleted.")
    else:
        messages.error(request, "The reported object could not be found.")
    
    return redirect('moderation')