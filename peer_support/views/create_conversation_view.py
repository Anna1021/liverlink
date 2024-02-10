from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from peer_support.models import Conversation,User
from peer_support.forms import ConversationForm, MessageForm

class CreateConversationView(LoginRequiredMixin, FormView):
    """Displays the user's conversation"""
    form_class = ConversationForm
    template_name = "create_conversation.html"

    def get(self,request):
        form = ConversationForm(request.user)
        return render(request,self.template_name,{'form':form,'user_conversations':request.user.conversations.all})

    def post(self,request):
        """Post request for user to send message to conversation"""
        form = ConversationForm(request.user,data = request.POST)
        if form.is_valid():
            conversation = form.save(request.user)
            return render(request,"conversation.html",{'form':MessageForm(conversation,user=request.user),'conversation':conversation,'user_conversations':request.user.conversations.all()})
        else:
            return render(request,self.template_name,{'form':form,'user_conversations':request.user.conversations.all})

        
