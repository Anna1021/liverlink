from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect,reverse
from peer_support.models import Conversation
from peer_support.forms import MessageForm
from django.views import View
from django.contrib import messages
from .helpers import conversation_does_not_exist,conversation_is_direct,no_conversation_url

class LeaveConversationView(LoginRequiredMixin,View):
    """User is removed from the group conversation"""
    def get(self,request,conversation_id):
        conversations = request.user.conversations.filter(id=conversation_id)
        if conversation_does_not_exist(request,conversations):
            return no_conversation_url(request)
        conversation = conversations[0]
        if conversation_is_direct(request,conversation):
            return redirect(reverse("conversation",kwargs={'conversation_id':conversation_id}))
        conversation.as_group().remove_user(request.user)
        return no_conversation_url(request)