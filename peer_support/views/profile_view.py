from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import User, UserProfile

class ProfileView(LoginRequiredMixin, View):
    """Displays other user's profile"""
    
    def get(self, request, username):
        """Get request for user to view profile"""
        user = User.objects.get(username=username)
        context = {'user': user}
        if hasattr(user, 'parent'):
            context['parent'] = user.parent
        elif hasattr(user, 'patient'):
            context['patient'] = user.patient
        else:
            context['mentor'] = user.mentor
        context['user_profile'] = UserProfile.objects.get(user=user)
        return render(request, 'profile.html', context)