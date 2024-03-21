from django.shortcuts import get_object_or_404, redirect, reverse
from peer_support.models import Report, Message, User, Post, PostComment
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class AcceptReportView(LoginRequiredMixin, View):
    """Delete report and remove object attached"""

    def get(self,request, report_id):
        if not request.user.is_staff:
            messages.error(request, "You do not have access to this view.")
            return redirect(reverse('feed'))
        report = get_object_or_404(Report, id=report_id)
        success = self.process_reported_object(report)
        if success:
            messages.success(request, "Report and the reported object have been successfully deleted.")
        else:
            messages.error(request, "The reported object could not be found.")
        return redirect('moderation')

    def process_reported_object(self, report):
        """Processes the reported object based on its type."""
        
        reported_object = report.content_object
        report.delete()
        if not reported_object:
            return False
        if isinstance(reported_object, Message):
            self.reported_message(reported_object)
        elif isinstance(reported_object, User):
            self.reported_user(reported_object)
        else:
            self.simple_delete(reported_object)            
        return True

    def reported_message(self, message):
        all_users = User.objects.all()  
        message.delete(all_users) 

    def reported_user(self, user):
        user.is_active = False
        user.save()
    
    def simple_delete(self,reported_object):
        reported_object.delete()
        
