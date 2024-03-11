from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import User
from django.views import View
from .helpers import get_conversation,no_conversation_url

class DeleteConversationView(LoginRequiredMixin,View):
    """User deletes conversation from their personal view"""
    def get(self,request,conversation_id):
        conversation = get_conversation(request,conversation_id)
        if not conversation:
            return no_conversation_url(request)
        users = User.objects.filter(username=request.user.username)
        conversation.delete(users)
        return no_conversation_url(request)