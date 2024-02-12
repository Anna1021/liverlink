from django.db import models
from django.utils import timezone
from peer_support.models import User

class Message(models.Model):
    """Model used for messages in a conversation"""
    sender = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,unique=False)
    content = models.CharField(max_length=100)
    send_time = models.DateTimeField(default=timezone.now)

    def delete(self):
        """Delete message"""
        Message.objects.filter(pk=self.pk).delete()

    def __str__(self):
        """Return a string representing the message"""
        return str(self.sender)+": "+self.content