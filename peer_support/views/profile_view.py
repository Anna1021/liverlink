from django.shortcuts import render,reverse,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import User, FriendRequest
from peer_support.forms import ReportForm
from django.contrib import messages
from .helpers import user_exists

class ProfileView(LoginRequiredMixin, View):
    """Displays other user's profile"""
    
    def get(self, request, username):
        """Get request for user to view profile"""

        if not user_exists(username):
            messages.error(request, "The profile you tried to access does not exist.")
            return redirect(reverse('dashboard'))
        user = User.objects.get(username=username)
        context = {
            'user': user, 'current_user': request.user,'blocklist': request.user.blocked_users.all() | user.blocked_users.all(),
            'is_friend': request.user in user.friends.all(),'report_form': ReportForm(), 'request_sent': FriendRequest.objects.filter(sender=request.user, receiver=user).exists(),
        }
        if hasattr(user, 'parent'):
            context['parent'] = user.parent
        elif hasattr(user, 'patient'):
            context['patient'] = user.patient
        else:
            context['mentor'] = user.mentor
        return render(request, 'profile.html', context)

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