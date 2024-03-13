from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from peer_support.models import Feedback

@login_required
def delete_feedback(request, feedback_id):
    """Delete a feedback object."""
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.delete()
    return redirect('feedback')