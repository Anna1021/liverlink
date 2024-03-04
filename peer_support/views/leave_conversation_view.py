from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect,reverse
from peer_support.models import Conversation
from peer_support.forms import MessageForm
from django.views import View
from django.contrib import messages

class LeaveConversationView(LoginRequiredMixin,View):
    """User is removed from the group conversation"""
    def get(self,request,conversation_id):
        conversations = request.user.conversations.filter(id=conversation_id)
        if conversations.count() == 0 or request.user not in conversations[0].users.all():
            messages.error(request,"This conversation does not exist.")
            context = {'user_conversations':request.user.sort_conversations()}
            return redirect(reverse('conversation',kwargs={'conversation_id':0}),context)
        conversation = conversations[0].as_group()
        if conversation is None:
            messages.error(request,"You cannot leave a direct conversation!")
            context = {
                'form':MessageForm(conversation,user=request.user),
                'conversation':conversation,
                'user_conversations':request.user.sort_conversations()
                }
            return redirect(reverse("conversation",kwargs={'conversation_id':conversation_id}),context)
        conversation.remove_user(request.user)
        context = {
            'user_conversations':request.user.sort_conversations()
            }
        return redirect(reverse("conversation",kwargs={'conversation_id':0}),context)