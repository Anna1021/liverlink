from django.db import models
from peer_support.models import User, Message
from django.apps import apps

class Conversation(models.Model):
    """Model used for direct conversations between two users"""
    users = models.ManyToManyField(User)
    messages = models.ManyToManyField(Message,blank=True)
    last_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        """Return a string representing the display name of the conversation"""
        members = self.users.all()
        return ", ".join([i.username for i in members]) 

    def add_users(self,users):
        """Add user to a group"""
        for user in users.all():
            self.users.add(user)
            user.conversations.add(self)

    def send(self,message):
        """Send message to the conversation"""
        self.messages.add(message)
        self.save()

    def as_group(self):
        """Return object as an instance of GroupConversation"""
        GroupConversation = apps.get_model('peer_support', 'GroupConversation')
        try:
            return self.groupconversation
        except GroupConversation.DoesNotExist:
            return None

    def get_first_member(self):
        """Return first member of the conversation"""
        return self.users.all()[0]

    def get_second_member(self):
        """Return second member of the conversation"""
        return self.users.all()[1]  

    def delete(self):
        """Delete conversation and its messages"""
        for message in self.messages.all():
            message.delete(self.users.all()) 
        Conversation.objects.filter(pk=self.pk).delete()  

