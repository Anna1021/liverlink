from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar

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
    unread_conversations = models.ManyToManyField('Conversation')


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

    def update_unread_conversations(self,conversation):
        self.unread_conversations.add(conversation)

class Message(models.Model):
    sender = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,unique=False)
    content = models.CharField(max_length=100)

class Conversation(models.Model):
    name = models.CharField(max_length=20,null=True)
    group = models.BooleanField()
    users = models.ManyToManyField(User)
    messages = models.ManyToManyField(Message)

    def display_name(self, current_user):
        if not self.group:
            other_member = self.users.exclude(username=current_user.username)[0]
            return other_member.username
        else:
            if self.name is None:
                members = self.users.all()
                return ", ".join([i.username for i in members]) #automatically ordered by username
            return self.name

    def add_user(self,user):
        if self.group:
            self.users.add(user)

    def remove_user(self,user):
        if self.group:
            self.users.remove(user)
            if self.users.count()==0:
                Message.objects.filter(pk=self.pk).delete() #completely deletes conversation if no member left

    def send(self,message):
        self.messages.add(message)
        for user in self.users.exclude(username=message.sender.username):
            user.update_unread_conversations(self)



    