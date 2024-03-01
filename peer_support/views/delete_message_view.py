from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from peer_support.models import Conversation, Message
from peer_support.forms import MessageForm
from django.contrib import messages

class DeleteMessageView(LoginRequiredMixin,View):
    """Deletes a message for either the user alone or for everyone in the conversation"""

    def get(self,request,conversation_id,message_id):
        conversations = Conversation.objects.filter(id=conversation_id)
        if conversations.count() == 0 or request.user not in conversations[0].users.all():
            messages.error(request,"This conversation does not exist.")
            context = {'user_conversations':request.user.sort_conversations()}
            return redirect(reverse('conversation',kwargs={'conversation_id':0}),context)
        conversation = conversations[0]
        conversation_messages = conversation.messages.filter(id=message_id)
        if conversation_messages.count() == 0 or request.user not in conversation_messages[0].visible_to.all():
            messages.error(request,"This message does not exist.")
            context = {'user_conversations':request.user.sort_conversations()}
            return redirect(reverse('conversation',kwargs={'conversation_id':0}),context)
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
