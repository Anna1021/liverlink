from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,reverse,redirect
from django.views.generic.edit import FormView
from peer_support.models import Conversation
from peer_support.forms import MessageForm
from .helpers import check_blocked_dm

class ConversationView(LoginRequiredMixin, FormView):
    """Displays the user's conversation"""
    form_class = MessageForm
    template_name = "conversation.html"

    def get(self,request,conversation_id):
        if conversation_id==0:
            return render(request,self.template_name,{'user_conversations':request.user.sort_conversations()})
        conversations = Conversation.objects.filter(id=conversation_id)
        if conversations.count() == 0:
            messages.error(request,"This conversation does not exist.")
            context = {'user_conversations':request.user.sort_conversations()}
            return redirect(reverse('conversation',kwargs={'conversation_id':0}),context)
        conversation = conversations.all()[0]
        current_user = request.user
        if current_user not in conversation.users.all():
            messages.error(request,"You do not have access to this conversation.")
            context = {'user_conversations':request.user.sort_conversations()}
            return redirect(reverse('conversation',kwargs={'conversation_id':0}),context)
        form = MessageForm(conversation,user=current_user)
        
        blocked_dm = check_blocked_dm(current_user, conversation)

        context = {"form":form, 'conversation':conversation,'user_conversations':request.user.sort_conversations(),'blocked_dm':blocked_dm}
        return render(request,self.template_name,context)

    def post(self,request,conversation_id):
        """Post request for user to send message to conversation"""
        conversation = Conversation.objects.get(id=conversation_id)
        form = MessageForm(conversation,data=request.POST,user=request.user)
        blocked_dm = check_blocked_dm(request.user, conversation)
        if form.is_valid() and request.user in conversation.users.all() and not blocked_dm:
            form.save()
            return render(request,self.template_name,{'form':MessageForm(conversation,user=request.user),'conversation':conversation,'user_conversations':request.user.sort_conversations()})
        elif blocked_dm:
            messages.error(request,"You cannot message this user.")
            return render(request,self.template_name,{'form':form,'conversation':conversation,'user_conversations':request.user.sort_conversations()}) 
        else:
            messages.error(request,"This message is not valid")
            return render(request,self.template_name,{'form':form,'conversation':conversation,'user_conversations':request.user.sort_conversations()})

        
