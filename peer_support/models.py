from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar
from django import template
from django.utils import timezone

class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    conversations = models.ManyToManyField('Conversation')
    unread_messages = models.ManyToManyField('Message')


    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        
        return self.gravatar(size=60)

    def update_unread_messages(self,message):
        self.unread_messages.add(message)

class Message(models.Model):
    sender = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,unique=False)
    content = models.CharField(max_length=100)
    send_time = models.DateTimeField(default=timezone.now)

class Conversation(models.Model):
    users = models.ManyToManyField(User)
    messages = models.ManyToManyField(Message)

    def add_user(self,user):
        """Adds user to a group"""
        self.users.add(user)

    def send(self,message):
        """Sends message to the conversation"""
        self.messages.add(message)
        for user in self.users.exclude(username=message.sender.username):
            user.update_unread_messages(message)

    def as_group(self):
        """Return object as an instance of GroupConversation"""
        try:
            return self.groupconversation
        except GroupConversation.DoesNotExist:
            return None

    def get_first_member(self):
        return self.users.all([0])

    def get_second_member(self):
        return self.users.all([1])    

class GroupConversation(Conversation):
    name = models.CharField(max_length=20,null=True)

    def remove_user(self,user):
        if self.group:
            self.users.remove(user)
            if self.users.count()==0:
                Message.objects.filter(pk=self.pk).delete() #completely deletes conversation if no member left

    def display_name(self):
        if self.name is None:
            members = self.users.all()
            return ", ".join([i.username for i in members]) #automatically ordered by username
        return self.name

    