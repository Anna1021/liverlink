from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import User

class OtherUserProfileView(LoginRequiredMixin, View):
    """Displays other user's profile"""
    
    def get(self, request, username):
        """Get request for user to view profile"""
        user = User.objects.get(username=username)
        context = {'user': user}
        return render(request, 'other_user_profile.html', context)