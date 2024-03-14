from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse
from peer_support.forms import ConversationForm, MessageForm
from peer_support.models import Notification

class CreateConversationView(LoginRequiredMixin, FormView):
    """Displays the user's conversation"""

    form_class = ConversationForm
    template_name = "create_conversation.html"

    def get(self, request):
        form = ConversationForm(request.user)
        return render(request, self.template_name, {'form': form, 'user_conversations': request.user.sort_conversations()})

    def post(self, request):
        """Post request for user to send message to conversation"""

        form = ConversationForm(request.user, data = request.POST)
        create_group = False
        if request.POST.get('group'):
            create_group = True
        if form.is_valid():
            conversation = form.save(request.user, create_group)
            self.send_notification(request.user, conversation)
            return redirect(reverse("conversation", kwargs={'conversation_id': conversation.id}), {'form': MessageForm(conversation, user=request.user), 'conversation': conversation, 'user_conversations': request.user.sort_conversations()})
        else:
            return render(request, self.template_name, {'form': form, 'user_conversations': request.user.sort_conversations()})
        
    def send_notification(self, request_user, conversation):
        """Sends notification to users in conversation"""
        
        for user in conversation.users.all().exclude(id=request_user.id):
            Notification.objects.create(
                title = "New conversation",
                description = f"You have been added to a new conversation by {request_user.username}.",
                user = user
            )