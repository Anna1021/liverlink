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
        context = { 'blocked_dm': blocked_dm, 'message_form': message_form, 'report_form': report_form , 'conversation': conversation, 'user_conversations': request.user.sort_conversations()}
        return render(request, self.template_name, context)

    def post(self, request, conversation_id):
        if 'report_message' in request.POST:
            message_id = request.POST.get('action')
            return self.handle_report_message(request, conversation_id,message_id)
        return self.handle_post_message(request, conversation_id)

    def handle_post_message(self, request, conversation_id):
        """Handles the post request for a message."""

        conversation = get_object_or_404(Conversation, id=conversation_id)
        message_form = MessageForm(conversation, data=request.POST, user=request.user)
        blocked_dm = check_blocked_dm(request.user, conversation)
        if message_form.is_valid() and request.user in conversation.users.all() and not blocked_dm:
            message_form.save()
            return redirect(reverse('conversation', kwargs={'conversation_id': conversation_id}))
        elif blocked_dm:
            messages.error(request,"You cannot message this user.")
            return redirect(reverse('conversation', kwargs={'conversation_id': conversation_id}))
        else:
            messages.error(request,"This message is not valid")
            return self.form_invalid(message_form) 

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
            messages.error(request, "There was an issue with the report.")
        return redirect(reverse('conversation', kwargs={'conversation_id': conversation_id}))
