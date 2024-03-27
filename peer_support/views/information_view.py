from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class InformationView(LoginRequiredMixin, View):
    """Displays information for the website"""

    def get(self, request):
        """Get request for user to view information"""

        return render(request, "information.html")
