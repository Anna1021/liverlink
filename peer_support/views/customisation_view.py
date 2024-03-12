import os
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

class CustomisationView(LoginRequiredMixin, View):
    """Displays user's customisation settings"""

    def get(self, request):
        """Get request for user to view customisation settings"""
        
        profile_pictures = os.listdir(os.path.join(settings.STATIC_ROOT, 'profile_pictures'))
        context = {'profile_pictures': profile_pictures}
        return render(request, 'customisation.html', context)