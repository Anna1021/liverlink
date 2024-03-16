from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse
from peer_support.forms import MessageForm
from django.views import View
from .helpers import get_conversation, conversation_is_direct, no_conversation_url

class LeaveConversationView(LoginRequiredMixin, View):
    """User is removed from the group conversation"""

    def get(self, request, conversation_id):
        conversation = get_conversation(request, conversation_id)
        if not conversation:
            return no_conversation_url(request)
        if conversation_is_direct(request, conversation):
            context = {
                'form':MessageForm(conversation, user=request.user),
                'conversation':conversation,
                'user_conversations':request.user.sort_conversations()
                }
            return redirect(reverse("conversation", kwargs={'conversation_id':conversation_id}), context)
        conversation.as_group().remove_user(request.user)
        return no_conversation_url(request)