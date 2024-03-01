from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,reverse,redirect
from django.views.generic.edit import FormView
from peer_support.models import Conversation
from peer_support.forms import MessageForm

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from peer_support.models import Report, Message 
from peer_support.forms import ReportForm 


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
        message_form = MessageForm(conversation,user=current_user)
        report_form = ReportForm()
        context = {"message_form":message_form, 'conversation':conversation,'user_conversations':request.user.sort_conversations()}
        return render(request,self.template_name,context)

    def post(self, request, conversation_id):
        action=request.POST.get('action')
        print(action)
        if action=='report_message':
            return self.handle_report_message(request,conversation_id)
        else:
            return self.handle_post_message(request,conversation_id)

    def handle_post_message(self,request,conversation_id):
        conversation = get_object_or_404(Conversation,id=conversation_id)
        form = MessageForm(conversation,data=request.POST,user=request.user)
        if form.is_valid() and request.user in conversation.users.all():
            form.save()
            return HttpResponseRedirect(reverse('conversation',kwargs={'conversation_id': conversation_id}))
        else:
            messages.error(request,"This message is not valid")
            return self.form_invalid(form) 

    def handle_report_message(self,request,conversation_id):
        message_id =request.POST.get('message_id')
        message =get_object_or_404(Message, id=message_id)
        report_form =ReportForm(request.POST)

        if report_form.is_valid():
            report =report_form.save(commit=False)
            report.message=message
            report.save()
            message.is_reported=True
            message.save()
            messages.success(request,"Message reported successfully.")
        else:
            messages.error(request,"There was an issue with the report.")
        
        return HttpResponseRedirect(reverse('conversation/0'))
