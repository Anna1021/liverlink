from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.shortcuts import redirect
from peer_support.models import User, Conversation

class GetConversationView(LoginRequiredMixin, View):
    """Get the direct conversation between two users; if none exist, create one."""

    def get(self, request, user_id):
        """Get the direct conversation between two users."""
        current_user = request.user
        second_user = User.objects.get(id=user_id)

        conversation = self.get_conversation(current_user, second_user)

        return redirect(reverse('conversation', kwargs={'conversation_id': conversation.id}))
    
    def create_conversation(self, current_user, second_user):
        """Create a direct conversation between two users."""
        conversation = Conversation.objects.create()
        conversation.users.add(current_user)
        conversation.users.add(second_user)
        current_user.conversations.add(conversation)
        second_user.conversations.add(conversation)
        return conversation
    
    def get_conversation(self, current_user, second_user):
        """Return a direct conversation between two users."""
        conversations = Conversation.objects.filter(users__in=[current_user]).filter(users__in=[second_user]).distinct()
        direct_conversations = []
        for conversation in conversations:
            if conversation.as_group() is None: direct_conversations.append(conversation)

        if direct_conversations == []:
            return self.create_conversation(current_user, second_user)
        else:
            return direct_conversations[0]
            