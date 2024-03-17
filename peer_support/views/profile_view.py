from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import User, FriendRequest
from peer_support.forms import ReportForm, ConversationForm
from django.contrib import messages
from .helpers import user_exists

class ProfileView(LoginRequiredMixin, View):
    """Displays user's profile"""
    
    def get(self, request, username):
        """Get request for user to view profile"""

        if not user_exists(username):
            messages.error(request, "The profile you tried to access does not exist.")
            return redirect(reverse('dashboard'))
        context = self.set_context(request, username)
        return render(request, 'profile.html', context)
    
    def get_user_type(self, user):
        if hasattr(user, 'parent'):
            return "PARENT"
        elif hasattr(user, 'patient'):
            return "PATIENT"
        elif hasattr(user, 'mentor'):
            return "MENTOR"
        else:
            return "ADMIN"

    def get_context(self, user, request):
        return {
            'user': user, 
            'current_user': request.user, 
            'blocklist': request.user.blocked_users.all() | user.blocked_users.all(),
            'is_friend': request.user in user.friends.all(), 
            'report_form': ReportForm(), 
            'request_sent': FriendRequest.objects.filter(sender=request.user, receiver=user).exists(),
            'user_type': self.get_user_type(user)
        }

    def set_context(self, request, username):
        """Classify the user and set context for the profile view"""
        
        user = User.objects.get(username=username)
        context = self.get_context(user, request)
        return context
    
    def post(self, request, username):
        """Handle POST requests for the ReportForm and ConversationForm."""

        if 'message' in request.POST:
            return self._handle_conversation_submission(request)
        elif 'report' in request.POST:
            return self._handle_report_submission(request, username)
        else:
            messages.error(request, "There was an issue with the report.")
        return redirect(reverse('profile', kwargs={'username': username}))

    def _handle_conversation_submission(self, request):
        """Handle conversation form submission."""

        conversation_form = ConversationForm(request.user, data=request.POST)
        conversation_form.fields['users'].queryset = User.objects.all()
        conversation = conversation_form.save(request.user)
        return redirect(reverse('conversation', kwargs={'conversation_id': conversation.id}))

    def _handle_report_submission(self, request, username):
        """Handle report form submission."""
        
        user = get_object_or_404(User, username=username)
        report_form = ReportForm(request.POST)
        if report_form.is_valid():
            report_form.save_report_for_object(user, request.user)
            messages.success(request, "Profile reported successfully.")
        else:
            messages.error(request, "There was an issue with the report.")
        return redirect(reverse('profile', kwargs={'username': username}))