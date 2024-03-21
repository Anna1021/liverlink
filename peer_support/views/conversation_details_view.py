from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.shortcuts import redirect, render
from django.urls import reverse
from peer_support.models import Conversation
from peer_support.forms import AddUsersForm
from .helpers import get_conversation, conversation_is_direct, no_conversation_url


class ConversationDetailsView(LoginRequiredMixin, FormView):
    """View group conversation details"""

    model = Conversation
    template_name = "conversation_details.html"

    def get_context_data(self, current_user, conversation):
        return {
            "conversation": conversation.as_group(),
            "user_conversations": current_user.sort_conversations(),
            "form": AddUsersForm(current_user, conversation.as_group()),
        }

    def get(self, request, conversation_id):
        conversation = get_conversation(request, conversation_id)
        if not conversation:
            return no_conversation_url(request)
        if conversation_is_direct(request, conversation):
            return redirect(reverse("conversation", kwargs={"conversation_id": conversation.id}), {"user_conversations": request.user.sort_conversations()})
        return render(request, self.template_name, self.get_context_data(request.user, conversation))

    def add_users(self, request, conversation):
        form = AddUsersForm(request.user, conversation, data=request.POST)
        if form.is_valid():
            form.save(conversation)
            return render(request, self.template_name, self.get_context_data(request.user, conversation))
        else:
            messages.error(request, "You have to add at least 1 person")
            return render(request, self.template_name, {"form": form, "conversation": conversation.as_group(), "user_conversations": request.user.sort_conversations()})

    def post(self, request, conversation_id):
        conversation = Conversation.objects.get(id=conversation_id).as_group()
        if "rename_conversation" in request.POST:
            new_name = request.POST.get("new_name")
            conversation.rename(new_name)
            return render(request, self.template_name, self.get_context_data(request.user, conversation))
        else:
            return self.add_users(request, conversation)
