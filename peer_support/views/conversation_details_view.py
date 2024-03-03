from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.shortcuts import redirect,render
from django.urls import reverse
from peer_support.models import Conversation
from peer_support.forms import AddUsersForm

class ConversationDetailsView(LoginRequiredMixin,FormView):
    """View group conversation details"""
    model = Conversation
    template_name = 'conversation_details.html' 

    def get_context_data(self,current_user,conversation):
        return {
            'conversation':conversation.as_group(),
            'user_conversations':current_user.sort_conversations(),
            'form': AddUsersForm(current_user,conversation.as_group())
        }

    def get(self,request, conversation_id):
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
        if conversation.as_group() is None:
            messages.error(request,"You can only do this for a group conversation")
            return redirect(reverse('conversation',kwargs={'conversation_id':conversation.id}),{'user_conversations':request.user.sort_conversations()})
        return render(request,self.template_name,self.get_context_data(request.user,conversation))

    def post(self,request, conversation_id):
        conversation = Conversation.objects.get(id=conversation_id).as_group()
        if 'rename_conversation' in  request.POST:
            new_name = request.POST.get('new_name')
            conversation.rename(new_name)
            return render(request,self.template_name,self.get_context_data(request.user,conversation))
        else:
            form = AddUsersForm(request.user,conversation,data=request.POST)
            if form.is_valid():
                form.save(conversation)
                return render(request,self.template_name,self.get_context_data(request.user,conversation))
            else:
                messages.error(request,"You have to add at least 1 person")
                return render(request,self.template_name,{'form':form,'conversation':conversation.as_group(),'user_conversations':request.user.sort_conversations()})#
