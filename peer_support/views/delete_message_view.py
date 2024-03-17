from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from peer_support.forms import MessageForm
from .helpers import get_conversation, get_message, no_conversation_url

class DeleteMessageView(LoginRequiredMixin, View):
    """Deletes a message for either the user alone or for everyone in the conversation"""

    def get(self, request, conversation_id, message_id):
        conversation = get_conversation(request, conversation_id)
        if not conversation:
            return no_conversation_url(request)
        message = get_message(request, conversation, message_id)
        if not message:
            return no_conversation_url(request)
        if request.GET.get('delete_all'):
            users = conversation.users.all()
        else:
            users = conversation.users.filter(username=request.user.username)
        message.delete(users)
        context = {
            'form':MessageForm(conversation, user=request.user),
            'conversation': conversation,
            'user_conversations': request.user.sort_conversations()
            }
        return redirect(reverse("conversation", kwargs={'conversation_id': conversation.id}), context)
