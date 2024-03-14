from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,reverse,redirect, get_object_or_404
from django.views.generic.edit import FormView
from .helpers import check_blocked_dm, conversation_does_not_exist, no_conversation_url, conversation_does_not_exist
from peer_support.models import Conversation, Message
from peer_support.forms import MessageForm, ReportForm
from django.core.paginator import Paginator

class ConversationView(LoginRequiredMixin, FormView):
    """Displays the user's conversation"""
    template_name = "conversation.html"

    def get(self,request,conversation_id,**kwargs):
        if conversation_id==0:
            return render(request,self.template_name,{'user_conversations':request.user.sort_conversations()})
        conversations = Conversation.objects.filter(id=conversation_id)
        if conversation_does_not_exist(request,conversations):
            return no_conversation_url(request)
        conversation = conversations[0]
        message_form = MessageForm(conversation,user=request.user)
        report_form = ReportForm()
        blocked_dm = check_blocked_dm(request.user, conversation)
        context = { 
            'blocked_dm':blocked_dm,
            'message_form':message_form, 
            'report_form':report_form , 
            'conversation':conversation,
            'user_conversations':request.user.sort_conversations(),
            'loaded_messages':self.load_messages(request,conversation)
            }
        return render(request,self.template_name,context)

    def post(self, request, conversation_id):
        delete=request.POST.get('delete')
        action=request.POST.get('action')
        if delete:
            return self.handle_delete_message(request,conversation_id,action,delete)
        elif action:
            return self.handle_report_message(request,conversation_id,action)
        else:
            return self.handle_post_message(request,conversation_id)

    def load_messages(self,request,conversation):
        message_id = request.GET.get('first_message')
        if not messages_to_load:
            message_index = 0
        else:
            message = essage =get_object_or_404(Message, id=message_id)
            message_index = list(conversation.messages.order_by("-id").filter(visible_to__in=[request.user])).index(message)
        message_index += 20
        return list(conversation.messages.filter(visible_to__in=[request.user]))[-message_index:]

    def handle_delete_message(self,request,conversation_id,message_id,delete):
        conversation = get_object_or_404(Conversation,id=conversation_id)
        message =get_object_or_404(Message, id=message_id)
        if delete == 'all':
            users = conversation.users.all()
        else:
            users = conversation.users.filter(username=request.user.username)
        message.delete(users)
        return redirect(reverse('conversation',kwargs={'conversation_id': conversation_id}))

    def handle_post_message(self,request,conversation_id):
        conversation = get_object_or_404(Conversation,id=conversation_id)
        message_form = MessageForm(conversation,data=request.POST,user=request.user)
        blocked_dm = check_blocked_dm(request.user, conversation)
        messages_to_load = int(request.POST.get('current_messages'))
        messages_to_load -= 20
        if message_form.is_valid() and request.user in conversation.users.all() and not blocked_dm:
            messages_to_load += 1
            message_form.save()
        elif blocked_dm:
            messages.error(request,"You cannot message this user.")
        else:
            messages.error(request,"This message is not valid")
        return redirect(reverse('conversation',kwargs={'conversation_id': conversation_id}))
        
    def handle_report_message(self,request,conversation_id,message_id):
        message =get_object_or_404(Message, id=message_id)
        report_form =ReportForm(request.POST)
        if report_form.is_valid():
            report_form.save_report_for_object(message,request.user)
            message.visible_to.remove(request.user)
            message.save()
            messages.success(request,"Message reported successfully.")
        else:
            messages.error(request,"There was an issue with the report.")
        return redirect(reverse('conversation',kwargs={'conversation_id': conversation_id}))