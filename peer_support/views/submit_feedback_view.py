from django.contrib import messages
from django.urls import reverse
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.forms import FeedbackForm

class SubmitFeedbackView(LoginRequiredMixin, FormView):
    """Displays the feedback form for users to submit feedback."""

    template_name = 'submit_feedback.html'
    form_class = FeedbackForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful feedback submission."""

        messages.add_message(self.request, messages.SUCCESS, "Feedback has been successfully submitted.")
        return reverse('feed')