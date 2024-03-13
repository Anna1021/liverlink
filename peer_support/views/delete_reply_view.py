from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden
from peer_support.models import Response

@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(Response, id=reply_id)
    if request.user == reply.user or request.user.is_superuser:
        question_id = reply.question.id
        reply.delete()
        return redirect(f'/question/{question_id}')
    else:
        return HttpResponseForbidden("You are not allowed to delete this reply.")
