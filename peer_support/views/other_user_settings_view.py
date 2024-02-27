from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class OtherUserSettingsView(LoginRequiredMixin, TemplateView):
    """Display the 'other users' section of profile settings."""

    template_name = 'other_user_settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['block_list'] = self.request.user.get_blocked_and_blocked_by_users()[0]
        return context