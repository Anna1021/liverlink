"""
from django.db import models
from peer_support.models import Conversation, Message

class GroupConversation(Conversation):
    name = models.CharField(max_length=20,null=True)

    def remove_user(self,user):
        if self.group:
            self.users.remove(user)
            if self.users.count()==0:
                Message.objects.filter(pk=self.pk).delete()

    def display_name(self):
        if self.name is None:
            members = self.users.all()
            return ", ".join([i.username for i in members])
        return self.name
"""