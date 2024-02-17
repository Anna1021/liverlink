from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect,render
from django.urls import reverse
from peer_support.models import Conversation

class ConversationDetailsView(LoginRequiredMixin,View):
    """View group conversation details"""
    model = Conversation
    template_name = 'conversation_details.html' 

    def get(self,request, conversation_id):
        conversation = Conversation.objects.get(id=conversation_id)
        if conversation.as_group() is None:
            messages.error("You can only do this for a group conversation")
            return redirect(reverse('conversation',kwargs={'conversation_id':conversation.id,'user_conversations':request.user.sort_conversations()}))
        return render(request,self.template_name,{'conversation':conversation.as_group(),'user_conversations':request.user.sort_conversations()})