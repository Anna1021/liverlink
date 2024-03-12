from django.shortcuts import render,reverse,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import User, FriendRequest
from peer_support.forms import ReportForm
from django.contrib import messages

class ProfileView(LoginRequiredMixin, View):
    """Displays user's profile"""
    
    def get(self, request, username):
        """Get request for user to view profile"""

        context = self.set_context(request,username)
        return render(request, 'profile.html', context)
    
    def set_context(self, request, username):
        """Classify the user and set context for the profile view"""

        user = User.objects.get(username=username)
        context = {'user': user, 'current_user': request.user}
        if hasattr(user, 'parent'):
            context['parent'] = user.parent
        elif hasattr(user, 'patient'):
            context['patient'] = user.patient
        else:
            context['mentor'] = user.mentor
        context['blocklist'] = request.user.blocked_users.all() | user.blocked_users.all()
        context['is_friend'] = request.user in user.friends.all()
        context['report_form'] = ReportForm()
        context['request_sent'] = FriendRequest.objects.filter(sender=request.user, receiver=user).exists()
        return context
    
    def post(self,request, username):
        """Reporting profile"""
        
        user =get_object_or_404(User, username=username)
        report_form =ReportForm(request.POST)
        if report_form.is_valid():
            report_form.save_report_for_object(user,request.user)
            messages.success(request,"Profile reported successfully.")
        else:
            messages.error(request,"There was an issue with the report.")
        return redirect(reverse('profile',kwargs={'username': username}))