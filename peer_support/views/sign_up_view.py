from django.conf import settings
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.urls import reverse
from peer_support.forms import SignUpForm
from .view_mixins import LoginProhibitedMixin
from .helpers import create_referral


class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        create_referral(self.object)
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
