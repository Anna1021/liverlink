from django.db import models
from peer_support.models import Conversation
class GroupConversation(Conversation):
    """Model used for group conversations between 2+ users"""
    name = models.CharField(max_length=20,null=True)

    def remove_user(self,user):
        """Remove user from group and delete self if no users in group"""
        self.users.remove(user)
        user.conversations.remove(self)
        if self.users.count()==0:
            self.delete() 

    def __str__(self):
        """Return a string representing the display name of the conversation"""
        if self.name is None:
            return super().__str__()
        return self.name