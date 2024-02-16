from django.db import models
from django.utils import timezone
from peer_support.models import User

class Message(models.Model):
    """Model used for messages in a conversation"""
    sender = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,unique=False)
    content = models.CharField(max_length=100)
    send_time = models.DateTimeField(default=timezone.now)
    visible_to = models.ManyToManyField(User, blank=True,related_name='visible_to')
    read_by = models.ManyToManyField(User, blank=True,related_name = 'read_by')

    def delete(self,users):
        """Delete message"""
        for user in users:
            self.visible_to.remove(user)
        if self.visible_to.count() == 0:
            Message.objects.filter(pk=self.pk).delete()

    def __str__(self):
        """Return a string representing the message"""
        return str(self.sender)+": "+self.content