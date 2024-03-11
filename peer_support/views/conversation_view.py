from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,reverse,redirect
from django.views.generic.edit import FormView
from peer_support.models import Conversation, Message
from peer_support.forms import MessageForm, ReportForm
from django.shortcuts import get_object_or_404
from .helpers import conversation_does_not_exist,no_conversation_url

class ConversationView(LoginRequiredMixin, FormView):
    """Displays the user's conversation"""
    template_name = "conversation.html"

    def get(self,request,conversation_id):
        if conversation_id==0:
            return render(request,self.template_name,{'user_conversations':request.user.sort_conversations()})
        conversations = Conversation.objects.filter(id=conversation_id)
        if conversation_does_not_exist(request,conversations):
            return no_conversation_url(request)
        conversation = conversations[0]
        message_form = MessageForm(conversation,user=request.user)
        report_form = ReportForm()
        context = {'message_form':message_form, 'report_form':report_form , 'conversation':conversation,'user_conversations':request.user.sort_conversations()}
        return render(request,self.template_name,context)

    def post(self,request,conversation_id):
        """Post request for user to send message to conversation"""
        conversation = Conversation.objects.get(id=conversation_id)
        form = MessageForm(conversation,data=request.POST,user=request.user)
        if form.is_valid() and request.user in conversation.users.all():
            form.save()
            return redirect(reverse('conversation',kwargs={'conversation_id':conversation.id}),{'form':MessageForm(conversation,user=request.user),'conversation':conversation,'user_conversations':request.user.sort_conversations()})
        else:
            messages.error(request,"This message is not valid")
            return self.form_invalid(message_form) 

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
