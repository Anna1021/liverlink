from django.db import models
from peer_support.models import User, Message

class Conversation(models.Model):
    users = models.ManyToManyField(User)
    messages = models.ManyToManyField(Message,blank=True)

    def __str__(self):
        members = self.users.all()
        return ", ".join([i.username for i in members]) 

    def add_user(self,user):
        """Adds user to a group"""
        self.users.add(user)

    def send(self,message):
        """Sends message to the conversation"""
        self.messages.add(message)
        # for user in self.users.exclude(username=message.sender.username):
        #     user.update_unread_messages(message)

    def as_group(self):
        """Return object as an instance of GroupConversation"""
        try:
            return self.groupconversation
        except GroupConversation.DoesNotExist:
            return None

    def get_first_member(self):
        return self.users.all()[0]

    def get_second_member(self):
        return self.users.all()[1]  

    def delete(self):
        for message in self.messages.all():
            message.delete() 
        Conversation.objects.filter(pk=self.pk).delete()  

class GroupConversation(Conversation):
    name = models.CharField(max_length=20,null=True)

    def remove_user(self,user):
        self.users.remove(user)
        if self.users.count()==0:
            self.delete() 

    def __str__(self):
        if self.name is None:
            return super().__str__()
        return self.name
