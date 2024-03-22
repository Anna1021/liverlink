from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic.edit import FormView
from .helpers import check_blocked_dm, no_conversation_url, get_conversation
from peer_support.models import Conversation, Message
from peer_support.forms import MessageForm, ReportForm

class ConversationView(LoginRequiredMixin, FormView):
    """Displays the user's conversation"""

    template_name = "conversation.html"

    def get(self, request, conversation_id):
        if conversation_id == 0:
            return render(request, self.template_name, {'user_conversations': request.user.sort_conversations()})
        conversation = get_conversation(request, conversation_id)
        if not conversation:
            return no_conversation_url(request)
        message_form = MessageForm(conversation, user=request.user)
        report_form = ReportForm()
        blocked_dm = check_blocked_dm(request.user, conversation)
        message_id = request.GET.get('first_message')
        first_message_id = self.first_message(request,conversation,message_id)
        next_message_id = self.next_message(request,conversation,first_message_id)
        context = { 
            'blocked_dm':blocked_dm,
            'message_form':message_form, 
            'report_form':report_form , 
            'conversation':conversation,
            'user_conversations':request.user.sort_conversations(),
            'first_message':first_message_id,
            'next_message':next_message_id
            }
        return render(request,self.template_name,context)

    def post(self, request, conversation_id):
        first_message_id = request.POST.get('first_message') or ''
        new_message = None
        delete=request.POST.get('delete')
        action=request.POST.get('action')
        if delete:
            self.handle_delete_message(request,conversation_id,action,delete)
        elif action:
            self.handle_report_message(request,conversation_id,action)
        else:
            new_message = self.handle_post_message(request,conversation_id)
        if new_message and first_message_id=='0':
            first_message_id = str(new_message.id)
        return redirect(reverse('conversation',kwargs={'conversation_id': conversation_id})+"?first_message="+first_message_id)

    def get_visible_messages(self,user,conversation):
        return conversation.messages.filter(visible_to__in=[user]).order_by('-id')

    def get_index_id(self,messages,index):
        if messages:
            return messages[index].id
        return 0

    def first_message(self,request,conversation,message_id):
        if not message_id or message_id=="0":
            return self.next_message(request,conversation,message_id)
        visible_messages = list(self.get_visible_messages(request.user,conversation).filter(id__gte=message_id))
        return self.get_index_id(visible_messages,-1)

    def next_message(self,request,conversation,message_id):
        visible_messages = list(self.get_visible_messages(request.user,conversation))
        if len(visible_messages)==0:
            return 0
        if not message_id or message_id=='' or message_id=='0':
            message_index = min(10,len(visible_messages))
        else:
            message = get_object_or_404(Message, id=message_id)
            message_index = visible_messages.index(message)
        message_index = min(message_index+10,len(visible_messages))
        next_message_id = self.get_index_id(visible_messages,message_index-1)
        return next_message_id

    def handle_delete_message(self,request,conversation_id,message_id,delete):
        conversation = get_object_or_404(Conversation,id=conversation_id)
        message =get_object_or_404(Message, id=message_id)
        if delete == 'all':
            users = conversation.users.all()
        else:
            users = conversation.users.filter(username=request.user.username)
        message.delete(users)


    def handle_post_message(self, request, conversation_id):
        """Handles the post request for a message."""

        conversation = get_object_or_404(Conversation, id=conversation_id)
        message_form = MessageForm(conversation, data=request.POST, user=request.user)
        blocked_dm = check_blocked_dm(request.user, conversation)
        if message_form.is_valid() and request.user in conversation.users.all() and not blocked_dm:
            return message_form.save()
        elif blocked_dm:
            messages.error(request,"You cannot message this user.")
        else:
            messages.error(request,"This message is not valid")
        
    def handle_report_message(self,request,conversation_id,message_id):
        """Handles the report request for a message."""

        message = get_object_or_404(Message, id=message_id)
        report_form = ReportForm(request.POST)
        if report_form.is_valid():
            report_form.save_report_for_object(message, request.user)
            message.visible_to.remove(request.user)
            message.save()
            messages.success(request, "Message reported successfully.")
        else:
            messages.error(request,"There was an issue with the report.")

