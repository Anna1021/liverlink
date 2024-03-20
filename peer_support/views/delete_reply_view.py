from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from peer_support.models import Response
from django.contrib import messages

@login_required
def delete_reply(request, reply_id):
    """Delete a reply."""

    try:
        reply = Response.objects.get(pk=reply_id)
    except Response.DoesNotExist:
        messages.error(request, 'The reply does not exist.')
        return redirect('resources')

    question_id = reply.question.id

    if request.user == reply.user or request.user.is_superuser:
        reply.delete()
        messages.success(request, 'The reply has been deleted successfully.')
        return redirect(reverse('question', kwargs={'id': question_id}))
    else:
        messages.error(request, 'You are not allowed to delete this reply.')
        return redirect(reverse('question', kwargs={'id': question_id}))
