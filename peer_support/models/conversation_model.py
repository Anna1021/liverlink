from django.db import models
from peer_support.models import User, Message

class Conversation(models.Model):
    """Model used for direct conversations between two users"""
    users = models.ManyToManyField(User)
    messages = models.ManyToManyField(Message,blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representing the display name of the conversation"""
        members = self.users.all()
        return ", ".join([i.username for i in members]) 

    def add_user(self,user):
        """Add user to a group"""
        self.users.add(user)

    def send(self,message):
        """Send message to the conversation"""
        self.messages.add(message)
        self.save()

    def as_group(self):
        """Return object as an instance of GroupConversation"""
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

class GroupConversation(Conversation):
    """Model used for group conversations between 2+ users"""
    name = models.CharField(max_length=20,null=True)

    def remove_user(self,user):
        """Remove user from group and delete self if no users in group"""
        self.users.remove(user)
        user.conversations.remove(self)
        if self.users.count()==0:
            self.delete() 

    def rename(self, new_name):
        """Rename conversation"""
        self.name = new_name
        if new_name == '':
            self.name = None
        self.save()

    def display_name(self):
        """Name displayed in the form for renaming conversations"""
        if self.name is None:
            return ""
        return self.name

    def __str__(self):
        """Return a string representing the display name of the conversation"""
        if self.name is None:
            return super().__str__()
        return self.name
