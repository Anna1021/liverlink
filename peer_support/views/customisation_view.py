import os
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles import finders


class CustomisationView(LoginRequiredMixin, View):
    """Displays user's customisation settings"""

    def get(self, request):
        """Get request for user to view customisation settings"""

        profile_pictures = self.get_profile_pictures()
        context = {"profile_pictures": profile_pictures}
        return render(request, "customisation.html", context)

    def get_profile_pictures(self):
        """Get all profile pictures from static files"""

        profile_pictures_dir = finders.find("profile_pictures", all=True)
        profile_pictures = []
        for dir in profile_pictures_dir:
            profile_pictures.extend(os.listdir(dir))
        return profile_pictures
