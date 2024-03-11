from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import User
from django.views import View
from .helpers import conversation_does_not_exist,no_conversation_url

class DeleteConversationView(LoginRequiredMixin,View):
    """User deletes conversation from their personal view"""
    def get(self,request,conversation_id):
        conversations = request.user.conversations.filter(id=conversation_id)
        if conversation_does_not_exist(request,conversations):
            return no_conversation_url(request)
        conversation = conversations[0]
        users = User.objects.filter(username=request.user.username)
        conversation.delete(users)
        return no_conversation_url(request)