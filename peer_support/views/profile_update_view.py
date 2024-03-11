from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse
from peer_support.models import Patient, Parent, Mentor, Professional
from peer_support.forms import UserForm, PatientForm, ParentForm, MentorForm, ProfessionalForm

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    template_name = "personal_information.html"

    def get_form_class(self):
        """Return form class based on model of current user."""
        if Patient.objects.filter(id=self.request.user.id).exists():
            return PatientForm
        elif Parent.objects.filter(id=self.request.user.id).exists():
            return ParentForm
        elif Mentor.objects.filter(id=self.request.user.id).exists():
            return MentorForm
        elif Professional.objects.filter(id=self.request.user.id).exists():
            return ProfessionalForm
        else:
            return UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user_id = self.request.user.id
        if Patient.objects.filter(id=user_id).exists():
            user = Patient.objects.get(id=user_id)
        elif Parent.objects.filter(id=user_id).exists():
            user = Parent.objects.get(id=user_id)
        elif Mentor.objects.filter(id=user_id).exists():
            user = Mentor.objects.get(id=user_id)
        elif Professional.objects.filter(id=user_id).exists():
            user = Professional.objects.get(id=user_id)
        else:
            user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)