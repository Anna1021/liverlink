from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render,redirect
# from django.views.generic.edit import FormView
from django.urls import reverse_lazy,reverse
from peer_support.models import Conversation,Message
from peer_support.forms import MessageForm


class DeleteMessageView(LoginRequiredMixin,View):

    def get(self,request,conversation_id,message_id):
        conversation = Conversation.objects.get(id=conversation_id)
        message = Message.objects.get(id=message_id)
        if request.POST.get('delete_all'):
            users = conversation.users.all()
        else:
            users = conversation.users.filter(username=request.user.username)
        message.delete(users)
        context = {
            'form':MessageForm(conversation,user=request.user),
            'conversation':conversation,
            'user_conversations':request.user.conversations.all()
            }
        return redirect(reverse("conversation",kwargs={'conversation_id':conversation.id}),context)
