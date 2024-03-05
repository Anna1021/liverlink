from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from peer_support.models import Conversation, Message
from peer_support.forms import MessageForm
from .helpers import conversation_does_not_exist,message_does_not_exist,no_conversation_url

class DeleteMessageView(LoginRequiredMixin,View):
    """Deletes a message for either the user alone or for everyone in the conversation"""

    def get(self,request,conversation_id,message_id):
        conversations = Conversation.objects.filter(id=conversation_id)
        if conversation_does_not_exist(request,conversations):
            return no_conversation_url(request)
        conversation = conversations[0]
        conversation_messages = conversation.messages.filter(id=message_id)
        if message_does_not_exist(request,conversation_messages):
            return no_conversation_url(request)
        message = conversation_messages[0]
        if request.GET.get('delete_all'):
            users = conversation.users.all()
        else:
            users = conversation.users.filter(username=request.user.username)
        message.delete(users)
        context = {
            'form':MessageForm(conversation,user=request.user),
            'conversation':conversation,
            'user_conversations':request.user.sort_conversations()
            }
        return redirect(reverse("conversation",kwargs={'conversation_id':conversation.id}),context)
