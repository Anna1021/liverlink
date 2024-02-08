from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from peer_support.models import Conversation
from peer_support.forms import MessageForm

class ConversationView(LoginRequiredMixin, FormView):
    """Displays the user's conversation"""
    form_class = MessageForm
    template_name = "conversation.html"

    def get(self,request,conversation_id):
        if conversation_id==0:
            return render(request,self.template_name,{'user_conversations':request.user.conversations.all()})
        conversation = Conversation.objects.get(id=conversation_id)
        current_user = request.user
        if current_user not in conversation.users.all():
            messages.error(request,"You do not have access to this conversation.")
            return reverse_lazy("conversation")
        form = MessageForm(conversation,user=current_user)
        print(request.user.conversations.all())
        context = {"form":form, 'conversation':conversation,'user_conversations':request.user.conversations.all()}
        return render(request,self.template_name,context)

    def post(self,request,conversation_id):
        """Post request for user to send message to conversation"""
        conversation = Conversation.objects.get(id=conversation_id)
        form = MessageForm(conversation,data=request.POST,user=request.user)
        if form.is_valid() and request.user in conversation.users.all():
            form.save()
            return render(request,self.template_name,{'form':MessageForm(conversation,user=request.user),'conversation':conversation,'user_conversations':request.user.conversations.all})
        else:
            messages.error(request,"This message is not valid")
            return render(request,self.template_name,{'form':form,'conversation':conversation,'user_conversations':request.user.conversations.all})

        
