import os
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from peer_support.models import User, UserProfile

class CustomisationView(LoginRequiredMixin, View):
    """Displays user's customisation settings"""

    def get(self, request):
        """Get request for user to view customisation settings"""
        user = User.objects.get(username=request.user)
        user_profile = UserProfile.objects.get(user=user)
        profile_pictures = os.listdir(os.path.join(settings.STATIC_ROOT, 'profile_pictures'))
        context = {'user': user, 'user_profile': user_profile, 'profile_pictures': profile_pictures}
        return render(request, 'customisation.html', context)